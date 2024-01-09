import json
from datetime import datetime

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
engine = create_engine('sqlite:///database/db/pmu_data.db')
Base.metadata.create_all(engine)
