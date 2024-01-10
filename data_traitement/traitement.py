from datetime import datetime
from database.database import save_pays, save_hippodrome, save_reunions, save_courses

def save_race_data(reunion_data):
    # Nettoyage des infos inutiles
    reunion_data.pop('parisEvenement', None)
    reunion_data.pop('meteo', None)
    reunion_data.pop('offresInternet', None)
    reunion_data.pop('regionHippique', None)
    reunion_data.pop('cagnottes', None)
    reunion_data['dateReunion'] = datetime.utcfromtimestamp(reunion_data['dateReunion'] / 1000.0)

    pays_data = reunion_data.get('pays', {})
    save_pays(pays_data)

    hippodrome_data = reunion_data.get('hippodrome', {})
    save_hippodrome(hippodrome_data)

    courses_data = reunion_data.get('courses', {})

    save_reunions(reunion_data)

    save_courses(courses_data)
