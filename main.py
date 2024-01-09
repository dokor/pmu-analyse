from datetime import datetime
from scrapping.scrapping import call_api_between_dates

# Example usage for a date range
start_date_param = datetime(2024, 1, 1)
end_date_param = datetime(2024, 1, 2)

call_api_between_dates(start_date_param, end_date_param)
