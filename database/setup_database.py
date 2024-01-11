from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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


class Participant(Base):
    __tablename__ = 'pmu_participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String)
    numPmu = Column(Integer)
    age = Column(Integer)
    sexe = Column(String)
    race = Column(String)
    statut = Column(String)
    oeilleres = Column(String)
    proprietaire = Column(String)
    entraineur = Column(String)
    driver = Column(String)
    driverChange = Column(Boolean)
    robe_code = Column(String)
    robe_libelleCourt = Column(String)
    robe_libelleLong = Column(String)
    indicateurInedit = Column(Boolean)
    musique = Column(String)
    nombreCourses = Column(Integer)
    nombreVictoires = Column(Integer)
    nombrePlaces = Column(Integer)
    nombrePlacesSecond = Column(Integer)
    nombrePlacesTroisieme = Column(Integer)
    gainsCarriere = Column(Float)
    gainsVictoires = Column(Float)
    gainsPlace = Column(Float)
    gainsAnneeEnCours = Column(Float)
    gainsAnneePrecedente = Column(Float)
    nomPere = Column(String)
    nomMere = Column(String)
    incident = Column(String)
    jumentPleine = Column(Boolean)
    engagement = Column(Boolean)
    supplement = Column(Float)
    handicapDistance = Column(Integer)
    handicapPoids = Column(Integer)
    poidsConditionMonteChange = Column(Boolean)
    dernierRapportDirect_typePari = Column(String)
    dernierRapportDirect_rapport = Column(Float)
    dernierRapportDirect_typeRapport = Column(String)
    dernierRapportDirect_indicateurTendance = Column(String)
    dernierRapportDirect_nombreIndicateurTendance = Column(Float)
    dernierRapportDirect_dateRapport = Column(DateTime)
    dernierRapportDirect_permutation = Column(Integer)
    dernierRapportDirect_favoris = Column(Boolean)
    dernierRapportDirect_numPmu1 = Column(Integer)
    dernierRapportDirect_grossePrise = Column(Boolean)
    dernierRapportReference_typePari = Column(String)
    dernierRapportReference_rapport = Column(Float)
    dernierRapportReference_typeRapport = Column(String)
    dernierRapportReference_indicateurTendance = Column(String)
    dernierRapportReference_nombreIndicateurTendance = Column(Float)
    dernierRapportReference_dateRapport = Column(DateTime)
    dernierRapportReference_permutation = Column(Integer)
    dernierRapportReference_favoris = Column(Boolean)
    dernierRapportReference_numPmu1 = Column(Integer)
    dernierRapportReference_grossePrise = Column(Boolean)
    urlCasaque = Column(String)
    commentaireApresCourse_texte = Column(String)
    commentaireApresCourse_source = Column(String)
    eleveur = Column(String)
    allure = Column(String)
    avisEntraineur = Column(String)

    # Relation avec la table Reunion
    # TODO

    # Relation avec la table Robe
    robe_id = Column(Integer, ForeignKey('pmu_robes.id'))
    robe = relationship("Robe")

    # Relation avec la table GainsParticipant
    gains_participant_id = Column(Integer, ForeignKey('pmu_gains_participants.id'))
    gains_participant = relationship("GainsParticipant")

    # Relation avec la table Rapport pour DernierRapportDirect
    dernier_rapport_direct_id = Column(Integer, ForeignKey('pmu_rapports.id'))
    dernier_rapport_direct = relationship("Rapport", foreign_keys=[dernier_rapport_direct_id])

    # Relation avec la table Rapport pour DernierRapportReference
    dernier_rapport_reference_id = Column(Integer, ForeignKey('pmu_rapports.id'))
    dernier_rapport_reference = relationship("Rapport", foreign_keys=[dernier_rapport_reference_id])

    # Relation avec la table Rapport pour DernierRapportReference
    dernier_rapport_reference_id = Column(Integer, ForeignKey('pmu_rapports.id'))
    dernier_rapport_reference = relationship("Rapport", foreign_keys=[dernier_rapport_reference_id])

    # Relation avec la table Allure
    allure_id = Column(Integer, ForeignKey('pmu_allures.id'))
    allure = relationship("Allure")

class Allure(Base):
    __tablename__ = 'allures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    libelleCourt = Column(String)
    libelleLong = Column(String)

class Robe(Base):
    __tablename__ = 'pmu_robes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    libelleCourt = Column(String)
    libelleLong = Column(String)

class GainsParticipant(Base):
    __tablename__ = 'pmu_gains_participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gainsCarriere = Column(Float)
    gainsVictoires = Column(Float)
    gainsPlace = Column(Float)
    gainsAnneeEnCours = Column(Float)
    gainsAnneePrecedente = Column(Float)

class Rapport(Base):
    __tablename__ = 'pmu_rapports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    typePari = Column(String)
    rapport = Column(Float)
    typeRapport = Column(String)
    indicateurTendance = Column(String)
    nombreIndicateurTendance = Column(Float)
    dateRapport = Column(DateTime)
    permutation = Column(Integer)
    favoris = Column(Boolean)
    numPmu1 = Column(Integer)
    grossePrise = Column(Boolean)


# Configurer la connexion à la base de données SQLite (utilisez un fichier local)
engine = create_engine('sqlite:///database/db/pmu_data.db')
Base.metadata.create_all(engine)
