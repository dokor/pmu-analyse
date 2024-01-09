# Exemple d'utilisation du script pour une course spécifique
from scrapping.scrapping import scrap_pmu_data

date_param = "01012024"
reunion_param = "r2"
course_param = "c1"

scrap_pmu_data(date_param, reunion_param, course_param)