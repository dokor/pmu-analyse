from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Reunion(Base):
    __tablename__ = 'reunions'

    id = Column(Integer, primary_key=True)
    cached = Column(Integer)
    timezoneOffset = Column(Integer)
    dateReunion = Column(DateTime)
    numOfficiel = Column(Integer)
    numOfficielReunionPrecedente = Column(Integer)
    numOfficielReunionSuivante = Column(Integer)
    numExterne = Column(Integer)
    nature = Column(String)
    audience = Column(String)
    statut = Column(String)
    disciplinesMere = Column(JSON)
    specialites = Column(JSON)
    derniereReunion = Column(String)
    reportPlusFpaMax = Column(Integer)
    hippodrome_code = Column(String, ForeignKey('hippodromes.code'))
    pays_code = Column(String, ForeignKey('pays.code'))
    nebulositeCode = Column(String)
    nebulositeLibelleCourt = Column(String)
    nebulositeLibelleLong = Column(String)
    temperature = Column(Integer)
    forceVent = Column(Integer)
    directionVent = Column(String)

class Hippodrome(Base):
    __tablename__ = 'hippodromes'

    code = Column(String, primary_key=True)
    libelleCourt = Column(String)
    libelleLong = Column(String)

class Pays(Base):
    __tablename__ = 'pays'

    code = Column(String, primary_key=True)
    libelle = Column(String)

# Configurer la connexion à la base de données SQLite (utilisez un fichier local)
engine = create_engine('sqlite:///pmu_data.db')
Base.metadata.create_all(engine)

# Créer une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Utiliser la session pour ajouter des données à la base de données
reunion_data = {...}  # Remplacez cela par les données de la réponse API
hippodrome_data = reunion_data.get('hippodrome', {})
pays_data = reunion_data.get('pays', {})

# Vérifier si les données existent déjà dans la base de données
existing_reunion = session.query(Reunion).filter_by(id=reunion_data['id']).first()
existing_hippodrome = session.query(Hippodrome).filter_by(code=hippodrome_data.get('code')).first()
existing_pays = session.query(Pays).filter_by(code=pays_data.get('code')).first()

# Ajouter les données uniquement si elles n'existent pas déjà
if not existing_reunion:
    reunion_obj = Reunion(**reunion_data, hippodrome_code=hippodrome_data.get('code'), pays_code=pays_data.get('code'))
    session.add(reunion_obj)

if not existing_hippodrome:
    hippodrome_obj = Hippodrome(**hippodrome_data)
    session.add(hippodrome_obj)

if not existing_pays:
    pays_obj = Pays(**pays_data)
    session.add(pays_obj)

# Committer les changements à la base de données
session.commit()
