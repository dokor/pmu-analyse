import logging
import requests
from datetime import timedelta
from data_traitement.traitement import save_race_data
from database.database import save_participants


# Calcul les dates intermédiaires entre deux dates données
def get_race_dates(start_date, end_date):
    current_date = start_date
    race_dates = []

    while current_date <= end_date:
        race_dates.append(current_date.strftime("%d%m%Y"))
        current_date += timedelta(days=1)

    return race_dates

# Apelle l'api pmu afin de récupérer l'ensemble des données des courses, réunions, hippodrome, participants
def call_api_between_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        reunion_number = 1
        while True:
            base_url = "https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{}/{}?specialisation=INTERNET"
            url = base_url.format(current_date.strftime("%d%m%Y"), f"R{reunion_number}")

            headers = {
                'accept': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            logging.debug(f"Attempting to call API for {current_date}, R{reunion_number}")
            response = requests.get(url, headers=headers)

            if response.status_code == 204:
                # The reunion does not exist
                logging.info(f"No more reunion [{reunion_number}] on {current_date} : 204")
                break
            elif response.status_code == 200:
                # Courses are available for this reunion
                data = response.json()
                logging.debug(f"Response 200 for reunions [R{reunion_number}] on {current_date}")
                save_race_data(data)
                scrap_participants(current_date, data)
            else:
                logging.error(f"API request failed. Status code: {response.status_code}, Date: {current_date}, Reunion: {reunion_number}")

            reunion_number += 1  # Move to the next reunion

        current_date += timedelta(days=1)  # Move to the next date


def scrap_participants(current_date, data):
    for course in data.get('courses'):
        base_url = "https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{}/{}/{}/participants?specialisation=INTERNET"
        url = base_url.format(current_date.strftime("%d%m%Y"), f"R{course.get('numReunion')}", f"C{course.get('numOrdre')}")

        headers = {
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        logging.debug(f"Attempting to call API for {current_date}, R{course.get('numReunion')}, C{course.get('numOrdre')}")
        response = requests.get(url, headers=headers)

        save_participants(response.json())
