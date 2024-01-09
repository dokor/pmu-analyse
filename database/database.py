from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database.setup_database import engine, Hippodrome, Pays, Reunion


def save_race_data(data):
    print("TRY SAVE")
    # Créer une session SQLAlchemy
    Session = sessionmaker(bind=engine)
    session = Session()

    # Utiliser la session pour ajouter des données à la base de données
    # TODO : remplacer par l'appel api
    #with open("../scrapping/scrapping_exemple.json", "r") as f:
    #    data = json.load(f)
    reunion_data = data

    # Nettoyage des infos inutiles
    reunion_data.pop('parisEvenement', None)
    reunion_data.pop('meteo', None)
    reunion_data.pop('offresInternet', None)
    reunion_data.pop('regionHippique', None)
    reunion_data.pop('cagnottes', None)
    reunion_data['dateReunion'] = datetime.utcfromtimestamp(reunion_data['dateReunion'] / 1000.0)


    hippodrome_data = reunion_data.get('hippodrome', {})
    pays_data = reunion_data.get('pays', {})

    # Vérifier si les données existent déjà dans la base de données
    existing_reunion = False
    existing_hippodrome = session.query(Hippodrome).filter_by(code=hippodrome_data.get('code')).first()
    existing_pays = session.query(Pays).filter_by(code=pays_data.get('code')).first()

    # Ajouter les données uniquement si elles n'existent pas déjà
    if not existing_pays:
        pays_obj = Pays(**pays_data)
        session.add(pays_obj)

    if not existing_hippodrome:
        hippodrome_obj = Hippodrome(**hippodrome_data)
        session.add(hippodrome_obj)

    if not existing_reunion:
        reunion_data.pop('hippodrome', None)
        reunion_data.pop('pays', None)
        reunion_data.pop('courses', None) # a adapter
        reunion_obj = Reunion(**reunion_data, hippodrome_code=hippodrome_data.get('code'), pays_code=pays_data.get('code'))
        session.add(reunion_obj)

    # Committer les changements à la base de données
    session.commit()
