from datetime import datetime
from logging.config import fileConfig
from scrapping.scrapping import call_api_between_dates

fileConfig('logger/logging_config.ini')

# Example usage for a date range
start_date_param = datetime(2024, 1, 1)
end_date_param = datetime(2024, 1, 9)

call_api_between_dates(start_date_param, end_date_param)
