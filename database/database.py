import logging
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database.setup_database import engine, Hippodrome, Pays, Reunion


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

    save_reunions(reunion_data)

def save_pays(pays_data):
    Session = sessionmaker(bind=engine)
    session = Session()
    existing_pays = session.query(Pays).filter_by(code=pays_data.get('code')).first()
    if not existing_pays:
        pays_obj = Pays(**pays_data)
        session.add(pays_obj)
        logging.info("Saving pays data")
    session.commit()

def save_hippodrome(hippodrome_data):
    Session = sessionmaker(bind=engine)
    session = Session()
    existing_hippodrome = session.query(Hippodrome).filter_by(code=hippodrome_data.get('code')).first()
    if not existing_hippodrome:
        hippodrome_obj = Hippodrome(**hippodrome_data)
        session.add(hippodrome_obj)
        logging.info("Saving hippodrome data")
    session.commit()

def save_reunions(reunion_data):
    Session = sessionmaker(bind=engine)
    session = Session()
    existing_reunion = (session.query(Reunion)
                        .filter_by(
        dateReunion=reunion_data.get('dateReunion'),
        numOfficiel=reunion_data.get('numOfficiel')
    ).first())
    if not existing_reunion:
        reunion_data.pop('hippodrome', None)
        reunion_data.pop('pays', None)
        reunion_data.pop('courses', None)
        reunion_obj = Reunion(**reunion_data, hippodrome_code=reunion_data.get('hippodrome', {}).get('code'), pays_code=reunion_data.get('pays', {}).get('code'))
        session.add(reunion_obj)
        logging.info("Saving reunion data")
    session.commit()
