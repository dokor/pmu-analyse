from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Reunion(Base):
    __tablename__ = 'pmu_reunions'

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
    hippodrome_code = Column(String, ForeignKey('pmu_hippodromes.code'))
    pays_code = Column(String, ForeignKey('pmu_pays.code'))
    nebulositeCode = Column(String)
    nebulositeLibelleCourt = Column(String)
    nebulositeLibelleLong = Column(String)
    temperature = Column(Integer)
    forceVent = Column(Integer)
    directionVent = Column(String)

class Hippodrome(Base):
    __tablename__ = 'pmu_hippodromes'

    code = Column(String, primary_key=True)
    libelleCourt = Column(String)
    libelleLong = Column(String)

class Pays(Base):
    __tablename__ = 'pmu_pays'

    code = Column(String, primary_key=True)
    libelle = Column(String)

class Course(Base):
    __tablename__ = 'pmu_courses'

    id = Column(Integer, primary_key=True)
    numReunion = Column(Integer)
    numOrdre = Column(Integer)
    libelle = Column(String)
    heureDepart = Column(DateTime)
    timezoneOffset = Column(Integer)
    distance = Column(Integer)
    distanceUnit = Column(String)
    corde = Column(String)
    nombreDeclaresPartants = Column(Integer)
    discipline = Column(String)
    specialite = Column(String)
    hippodrome_code = Column(String, ForeignKey('pmu_hippodromes.code'))
    ordreArrivee= Column(JSON)
    # incidents = Column(String)

    # Add other fields as needed

    # Define a relationship with the Pari model
    # paris = relationship('Pari', back_populates='pmu_courses')

# class Pari(Base):
#     __tablename__ = 'pmu_paris'
#
#     id = Column(Integer, primary_key=True)
#     numReunion = Column(Integer, ForeignKey('courses.numReunion'))
#     numExterneReunion = Column(Integer, ForeignKey('courses.numExterneReunion'))
#     codePari = Column(String)
#     # Add other fields as needed
#
#     # Define a relationship with the Course model
#     course = relationship('Course', back_populates='pmu_paris')

# class Cheval(Base):
#     __tablename__ = 'pmu_cheval'
#
#     code = Column(String, primary_key=True)
#     libelle = Column(String)

# Configurer la connexion à la base de données SQLite (utilisez un fichier local)
engine = create_engine('sqlite:///database/db/pmu_data.db')
Base.metadata.create_all(engine)
