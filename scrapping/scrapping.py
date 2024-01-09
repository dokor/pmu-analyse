import requests
from datetime import datetime, timedelta

from database.database import save_race_data

def call_api(date, reunion, course):
    base_url = "https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{}/{}/{}?specialisation=INTERNET"
    url = base_url.format(date, reunion, course)

    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        # Ajoutez d'autres en-têtes au besoin
    }

    # Envoyer une requête GET à l'URL de l'API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Convertir la réponse JSON en un dictionnaire Python
        data = response.json()

        print("Tentative de save de la course", reunion, course, date)
        # Appeler la fonction d'analyse de la course avec les données de l'API
        #save_race_data(data)

    else:
        print("Échec de la requête API. Code de statut:", response.status_code)

def get_race_dates(start_date, end_date):
    current_date = start_date
    race_dates = []

    while current_date <= end_date:
        race_dates.append(current_date.strftime("%d%m%Y"))
        current_date += timedelta(days=1)

    return race_dates

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
                # Add other headers as needed
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 204:
                # No more courses for this reunion or the reunion does not exist
                break
            elif response.status_code == 200:
                # Courses are available for this reunion
                data = response.json()
                save_race_data(data)
            else:
                print(f"Failed API request for date {current_date}, reunion {reunion_number}. Status code:", response.status_code)
                # Handle other status codes as needed
            reunion_number += 1  # Move to the next reunion

        current_date += timedelta(days=1)  # Move to the next date
