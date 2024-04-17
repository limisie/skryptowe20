from L5_API.constants import DB_LIMITS
from L5_API.db_manager import get_rates_dates_interpolated, get_sales_and_dates


def get_rates_ipd(code, date_from, date_to):
    data = get_rates_dates_interpolated(code, date_from, date_to)
    data = [{"date": data[1][i], "rate": data[0][i], "ipd": data[2][i]} for i in range(len(data[0]))]
    return data


def get_sales(date_from, date_to):
    data = get_sales_and_dates(date_from, date_to)
    data = [{"date": data[2][i], "total_usd": data[0][i], "total_pln": data[1][i]} for i in range(len(data[0]))]
    return data


def get_rates_limits(code):
    date_min = DB_LIMITS[code.upper()]['date_min']
    date_max = DB_LIMITS[code.upper()]['date_max']
    return date_min, date_max


def get_sales_limits():
    date_min = DB_LIMITS['SALES']['date_min']
    date_max = DB_LIMITS['SALES']['date_max']
    return date_min, date_max
