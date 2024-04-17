import unittest
from datetime import datetime

from L4_API.api_handler import _get_table, currency_rates_and_dates_time_frame, _are_dates, \
    currency_rates_and_dates_from_last_days
from L4_API.db_handler import data_to_plot, get_sales_and_dates, get_sale_and_date, get_rate_and_date, \
    get_rates_and_dates


class TestApiMethods(unittest.TestCase):

    def test_table_getter(self):
        table = _get_table('USD')
        self.assertEqual(table, 'A')

        table = _get_table('JOD')
        self.assertEqual(table, 'B')

        table = _get_table('sdgdf')
        self.assertEqual(table, '')

        table = _get_table('')
        self.assertEqual(table, '')

        table = _get_table(78)
        self.assertEqual(table, '')

    def test_dates_validation(self):
        date_from, date_to = ('2021-01-01', '2021-01-10')
        self.assertTrue(_are_dates(date_from, date_to))
        self.assertFalse(_are_dates(date_to, date_from))

        date_from, date_to = ('2021-01-01', '2021-01-01')
        self.assertTrue(_are_dates(date_from, date_to))

        date_from, date_to = ('', '2021-01-01')
        self.assertFalse(_are_dates(date_from, date_to))

        date_from, date_to = ('', '')
        self.assertFalse(_are_dates(date_from, date_to))

    def test_currency_rates_and_dates(self):
        rates, dates = currency_rates_and_dates_time_frame('USD', '2020-01-01', '2020-01-01')
        self.assertEqual(len(rates), 1)
        self.assertEqual(dates, ['2020-01-01'])

        rates, dates = currency_rates_and_dates_time_frame('USD', '2020-01-01', '2020-01-02')
        self.assertEqual(len(rates), 2)
        self.assertEqual(dates, ['2020-01-01', '2020-01-02'])

        rates, dates = currency_rates_and_dates_time_frame('USD', '2020-01-01', '2020-01-10')
        self.assertEqual(len(rates), 10)

        rates, dates = currency_rates_and_dates_time_frame('USD', '2020-01-01', '2020-01-10')
        self.assertEqual(len(rates), 10)

        rates, dates = currency_rates_and_dates_from_last_days('USD', 0)
        self.assertEqual(rates, [])
        self.assertEqual(dates, [])

        rates, dates = currency_rates_and_dates_from_last_days('USD', -1)
        self.assertEqual(rates, [])
        self.assertEqual(dates, [])

        rates, dates = currency_rates_and_dates_from_last_days('df', 1)
        self.assertEqual(rates, [])
        self.assertEqual(dates, [])

        rates, dates = currency_rates_and_dates_from_last_days(2, 1)
        self.assertEqual(rates, [])
        self.assertEqual(dates, [])

        rates, dates = currency_rates_and_dates_from_last_days('USD', 1)
        self.assertEqual(len(rates), 1)
        self.assertEqual(len(dates), 1)

    def test_one_day_interpolated(self):
        rates, dates = currency_rates_and_dates_time_frame('USD', '2020-01-01', '2020-01-01')
        self.assertEqual(len(rates), 1)
        self.assertEqual(dates, ['2020-01-01'])

    def test_weekend_interpolated(self):
        rates, dates = currency_rates_and_dates_time_frame('USD', '2020-01-09', '2020-01-10')
        self.assertEqual(len(rates), 2)
        self.assertEqual(dates, ['2020-01-09', '2020-01-10'])

    def test_one_day(self):
        rates, dates = currency_rates_and_dates_time_frame('USD', '2020-01-12', '2020-01-12')
        self.assertEqual(len(rates), 1)
        self.assertEqual(dates, ['2020-01-12'])


class TestDbMethods(unittest.TestCase):

    def test_get_sales(self):
        sales, dates = get_sale_and_date('2009-01-01')
        self.assertEqual(sales, [1.98])

        sales, dates = get_sale_and_date('2009-01-04')
        self.assertEqual(sales, [])

        sales, dates = get_sales_and_dates('2010-01-01', '2010-01-31')
        self.assertEqual(len(sales), len(dates))

    def test_get_rates(self):
        rate, date = get_rate_and_date('2009-01-02', 'USD')
        self.assertEqual(rate[0], 2.991)

        date_from = '2010-01-01'
        date_to = '2010-01-31'
        rates, dates = get_rates_and_dates('USD', date_from, date_to)
        delta = (datetime.strptime(date_to, '%Y-%m-%d') - datetime.strptime(date_from, '%Y-%m-%d')).days + 1
        self.assertEqual(dates[0], date_from)
        self.assertEqual(dates[-1], date_to)
        self.assertEqual(len(rates), len(dates))
        self.assertEqual(len(rates), delta)

    def test_get_sales_invalid_values(self):
        date_from = '2010-01-01'
        date_to = '2010-01-31'

        sales, dates = get_sale_and_date('')
        self.assertEqual(sales, [])

        sales, dates = get_sale_and_date('3sfsr')
        self.assertEqual(sales, [])

        sales, dates = get_sale_and_date('2020-12-31')
        self.assertEqual(sales, [])

        sales, dates = get_sales_and_dates(date_to, date_from)
        self.assertEqual(dates, [])
        self.assertEqual(sales, [])

    def test_data_to_plot(self):
        code = 'USD'
        date_from = '2010-01-01'
        date_to = '2010-01-31'

        dates, sales_usd, sales_pln = data_to_plot(code, date_from, date_to)
        self.assertEqual(dates[0], date_from)
        self.assertEqual(dates[-1], date_to)
        self.assertEqual(len(sales_usd), len(sales_pln))
        self.assertEqual(len(sales_usd), len(dates))
