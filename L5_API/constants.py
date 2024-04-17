import os

DATE_FORMAT = "%Y-%m-%d"
DATA_LIMIT = 365
MAX_TRIES = 10

CURRENCIES = ['USD', 'EUR', 'GBP']
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sales.db')

DB_LIMITS = {'USD': {'date_min': '2009-01-01', 'date_max': '2021-01-19'},
             'EUR': {'date_min': '2009-01-01', 'date_max': '2021-01-19'},
             'GBP': {'date_min': '2009-01-01', 'date_max': '2021-01-19'},
             'SALES': {'date_min': '2009-01-01', 'date_max': '2013-12-22'}}

HOUR_LIMIT = '100 per hour'
DAY_LIMIT = '1000 per day'
USER_LIMIT = '1 per second'

CACHE_TIMEOUT = 86400
