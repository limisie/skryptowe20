import L4_API.api_handler as api_hdl
import L4_API.db_handler as db_hdl

CURRENCIES = ['USD', 'EUR', 'CHF']
YEAR = 365


def get_rates_from_last_days(currency_code, days):
    rates, dates = api_hdl.currency_rates_and_dates_from_last_days(currency_code, days)
    return rates, dates


def get_rate(currency_code, date):
    rate, date = api_hdl.currency_rates_and_dates_time_frame(currency_code, date, date)
    return rate, date


def get_rates(currency_code, date_from, date_to):
    rates, dates = api_hdl.currency_rates_and_dates_time_frame(currency_code, date_from, date_to)
    return rates, dates


def plot_rates(currency_codes, days):
    api_hdl.plot(currency_codes, days)


def plot_sales(currency_code, date_from, date_to):
    db_hdl.plot_sale_time_frame(currency_code, date_from, date_to)


def add_rates_to_db(currency_code, date_from, date_to):
    rates, dates = api_hdl.currency_rates_and_dates_time_frame(currency_code, date_from, date_to)
    db_hdl.add_rate_entries(dates, rates, currency_code)


if __name__ == '__main__':
    plot_rates(CURRENCIES, YEAR // 2)
    plot_sales('USD', '2011-01-01', '2011-12-31')
