from datetime import datetime

from L5_API import db_app
from L5_API.constants import CURRENCIES, DATE_FORMAT, DATA_LIMIT


def is_code(code):
    return code.upper() in CURRENCIES


def are_dates(date_from, date_to):
    dates = True

    try:
        datetime.strptime(date_from, DATE_FORMAT)
        datetime.strptime(date_to, DATE_FORMAT)
    except ValueError:
        dates = False

    return dates


def are_dates_chronological(date_from, date_to):
    return date_from <= date_to


def are_in_limit(date_from, date_to, code):
    if code == 'NONE':
        date_min, date_max = db_app.get_sales_limits()
    else:
        date_min, date_max = db_app.get_rates_limits(code)

    date_min = datetime.strptime(date_min, DATE_FORMAT).date()
    date_max = datetime.strptime(date_max, DATE_FORMAT).date()

    return date_min <= date_to <= date_max and date_min <= date_from <= date_max


def are_in_range(date_from, date_to):
    return (date_to - date_from).days < DATA_LIMIT


def validate_dates(date_from, date_to, code='NONE'):
    if not are_dates(date_from, date_to):
        return False, '400 BadRequest - Wrong format of dates - should be 0000-00-00', 400

    date_from = datetime.strptime(date_from, DATE_FORMAT).date()
    date_to = datetime.strptime(date_to, DATE_FORMAT).date()

    if not are_dates_chronological(date_from, date_to):
        return False, '400 BadRequest - Invalid date range - endDate is before startDate', 400

    if not are_in_limit(date_from, date_to, code):
        return False, '400 BadRequest - Invalid date range - date outside the database limit', 400

    if not are_in_range(date_from, date_to):
        return False, '400 BadRequest - Limit of {} days has been exceeded'.format(DATA_LIMIT), 400

    return True, '', 200


def validate_date(date, code='NONE'):
    return validate_dates(date, date, code)
