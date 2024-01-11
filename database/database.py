import logging
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from database.setup_database import engine, Hippodrome, Pays, Reunion, Course, Participant, Robe, Rapport


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

def save_courses(courses_data):
    for course_data in courses_data:
        Session = sessionmaker(bind=engine)
        session = Session()
        course_data['heureDepart'] = datetime.utcfromtimestamp(course_data['heureDepart'] / 1000.0)
        existing_course = (session.query(Course).filter_by(
            heureDepart=course_data.get('heureDepart'),
            numReunion=course_data.get('numReunion'),
            numOrdre=course_data.get('numOrdre')
        ).first())
        if not existing_course:
            hipodrome_code = course_data.get('hippodrome', {}).get('codeHippodrome')
            # Définissez une liste des noms d'attributs valides de la classe Course
            valid_attributes = [attr.name for attr in Course.__table__.columns]

            # Créez un nouveau dictionnaire avec seulement les attributs valides
            filtered_course_data = {key: value for key, value in course_data.items() if key in valid_attributes}

            course_obj = Course(**filtered_course_data, hippodrome_code=hipodrome_code)
            session.add(course_obj)
            logging.info("Saving Course data")
            session.commit()

def save_participants(participant_data):
    for participant in participant_data.get('participants'):
        save_participant(participant)
def save_participant(participant_data):
    # Récupérer la session SQLAlchemy
    Session = sessionmaker(bind=engine)
    session = Session()

    # Traitement de l'objet 'robe'
    robe_data = participant_data.get('robe', {})
    robe_obj = session.query(Robe).filter_by(**robe_data).first()
    if not robe_obj:
        robe_obj = Robe(**robe_data)
        session.add(robe_obj)
        session.commit()
        logging.info("Saving Robe data")

    # Traitement de l'objet 'dernierRapportDirect'
    dernier_rapport_direct_data = participant_data.get('dernierRapportDirect', {})
    dernier_rapport_direct_obj = session.query(Rapport).filter_by(**dernier_rapport_direct_data).first()
    if not dernier_rapport_direct_obj:
        dernier_rapport_direct_obj = Rapport(**dernier_rapport_direct_data)
        session.add(dernier_rapport_direct_obj)
        session.commit()
        logging.info("Saving DernierRapportDirect data")

    # Traitement de l'objet 'dernierRapportReference'
    dernier_rapport_reference_data = participant_data.get('dernierRapportReference', {})
    dernier_rapport_reference_obj = session.query(Rapport).filter_by(**dernier_rapport_reference_data).first()
    if not dernier_rapport_reference_obj:
        dernier_rapport_reference_obj = Rapport(**dernier_rapport_reference_data)
        session.add(dernier_rapport_reference_obj)
        session.commit()
        logging.info("Saving DernierRapportReference data")

    # Retirer les sous-objets du participant_data pour éviter les erreurs
    participant_data.pop('robe', None)
    participant_data.pop('dernierRapportDirect', None)
    participant_data.pop('dernierRapportReference', None)

    # Vérifier si le participant existe déjà
    participant_obj = session.query(Participant).filter_by(**participant_data).first()
    if not participant_obj:
        # Créer l'objet Participant avec les données restantes
        participant_obj = Participant(**participant_data)

        # Liaison entre le Participant et les sous-objets
        participant_obj.robe = robe_obj
        participant_obj.dernierRapportDirect = dernier_rapport_direct_obj
        participant_obj.dernierRapportReference = dernier_rapport_reference_obj

        # Enregistrement du Participant
        session.add(participant_obj)
        session.commit()
        logging.info("Saving Participant data")


# Récupération de la course en BDD
def fetch_course():
    Session = sessionmaker(bind=engine)
    session = Session()
    #return (session.query(Course).filter_by(
    #    heureDepart=course_data.get('heureDepart'),
    #    numReunion=course_data.get('numReunion'),
    #    numOrdre=course_data.get('numOrdre')
    #).first())