import json
import unittest
from datetime import datetime

import requests

from L5_API.constants import DB_LIMITS, DATE_FORMAT

BASE = 'http://127.0.0.1:5000/'


class TestLastRate(unittest.TestCase):

    def test_valid_code_usd(self):
        code = 'USD'
        response = requests.get(BASE + '/rates/' + code)
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(code, response_data['Currency Code'])
        self.assertEqual(DB_LIMITS[code]['date_max'], response_data['Rates']['Rate']['Date'])
        self.assertEqual(3.6322, response_data['Rates']['Rate']['Rate'])
        self.assertEqual(False, response_data['Rates']['Rate']['Interpolated'])

    def test_valid_code_eur(self):
        code = 'EUR'
        response = requests.get(BASE + '/rates/' + code)
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(code, response_data['Currency Code'])
        self.assertEqual(DB_LIMITS[code]['date_max'], response_data['Rates']['Rate']['Date'])
        self.assertEqual(4.4348, response_data['Rates']['Rate']['Rate'])
        self.assertEqual(False, response_data['Rates']['Rate']['Interpolated'])

    def test_invalid_code(self):
        code = 'dsf'
        response = requests.get(BASE + '/rates/' + code)
        status_code = response.status_code

        self.assertEqual(404, status_code)

    def test_empty_code(self):
        code = ''
        response = requests.get(BASE + '/rates/' + code)
        status_code = response.status_code

        self.assertEqual(404, status_code)


class TestRateLimit(unittest.TestCase):

    def test_valid_code_usd(self):
        code = 'USD'
        response = requests.get(BASE + '/rates/' + code + '/limits')
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(code, response_data['Currency Code'])
        self.assertEqual(DB_LIMITS[code]['date_min'], response_data['Limits']['Lower date limit'])
        self.assertEqual(DB_LIMITS[code]['date_max'], response_data['Limits']['Upper date limit'])

    def test_valid_code_eur(self):
        code = 'EUR'
        response = requests.get(BASE + '/rates/' + code + '/limits')
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(code, response_data['Currency Code'])
        self.assertEqual(DB_LIMITS[code]['date_min'], response_data['Limits']['Lower date limit'])
        self.assertEqual(DB_LIMITS[code]['date_max'], response_data['Limits']['Upper date limit'])

    def test_invalid_code(self):
        code = 'sfd'
        response = requests.get(BASE + '/rates/' + code + '/limits')
        status_code = response.status_code

        self.assertEqual(404, status_code)

    def test_empty_code(self):
        code = ''
        response = requests.get(BASE + '/rates/' + code + '/limits')
        status_code = response.status_code

        self.assertEqual(404, status_code)


class TestRates(unittest.TestCase):

    def test_valid_code_usd(self):
        code = 'USD'
        date_from = '2020-01-01'
        date_to = '2020-01-10'
        delta = (datetime.strptime(date_to, DATE_FORMAT).date() - datetime.strptime(date_from, DATE_FORMAT).date()).days
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(code, response_data['Currency Code'])
        self.assertEqual(date_from, response_data['Rates']['1']['Date'])
        self.assertEqual(date_to, response_data['Rates'][str(delta + 1)]['Date'])
        self.assertEqual(delta + 1, len(response_data['Rates']))

    def test_valid_code_eur(self):
        code = 'EUR'
        date_from = '2010-01-01'
        date_to = '2010-02-10'
        delta = (datetime.strptime(date_to, DATE_FORMAT).date() - datetime.strptime(date_from, DATE_FORMAT).date()).days
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(code, response_data['Currency Code'])
        self.assertEqual(date_from, response_data['Rates']['1']['Date'])
        self.assertEqual(date_to, response_data['Rates'][str(delta + 1)]['Date'])
        self.assertEqual(delta + 1, len(response_data['Rates']))

    def test_invalid_code(self):
        code = 'efe'
        date_from = '2020-01-01'
        date_to = '2020-01-10'
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        status_code = response.status_code

        self.assertEqual(404, status_code)

    def test_empty_code(self):
        code = ''
        date_from = '2020-01-01'
        date_to = '2020-01-10'
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        status_code = response.status_code

        self.assertEqual(404, status_code)

    def test_one_date(self):
        code = 'USD'
        date_from = '2020-01-01'
        date_to = '2020-01-01'
        delta = (datetime.strptime(date_to, DATE_FORMAT).date() - datetime.strptime(date_from, DATE_FORMAT).date()).days
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(code, response_data['Currency Code'])
        self.assertEqual(date_from, response_data['Rates']['1']['Date'])
        self.assertEqual(date_to, response_data['Rates'][str(delta + 1)]['Date'])
        self.assertEqual(delta + 1, len(response_data['Rates']))
        self.assertEqual(1, len(response_data['Rates']))

    def test_invalid_dates_non_chronological(self):
        code = 'USD'
        date_from = '2020-01-03'
        date_to = '2020-01-01'
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)

    def test_invalid_dates(self):
        code = 'USD'
        date_from = 'sfs'
        date_to = '2020-01-01'
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)

    def test_empty_dates(self):
        code = 'USD'
        date_from = ''
        date_to = ''
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        status_code = response.status_code

        self.assertEqual(404, status_code)

    def test_invalid_dates_outside_limits(self):
        code = 'USD'
        date_from = '2000-01-01'
        date_to = '2000-01-03'
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)

    def test_invalid_dates_outside_range(self):
        code = 'USD'
        date_from = '2000-01-01'
        date_to = '2020-01-03'
        response = requests.get(BASE + '/rates/{}/{}/{}'.format(code, date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)


class TestSale(unittest.TestCase):

    def test_valid_date(self):
        date = '2009-01-03'
        response = requests.get(BASE + '/sales/' + date)
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(date, response_data['Sales']['1']['Date'])
        self.assertEqual(5.94, response_data['Sales']['1']['USD Total'])
        self.assertEqual(1, len(response_data['Sales']))


class TestSalesLimit(unittest.TestCase):

    def test(self):
        response = requests.get(BASE + '/sales/limits')
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(DB_LIMITS['SALES']['date_min'], response_data['Sales']['Lower date limit'])
        self.assertEqual(DB_LIMITS['SALES']['date_max'], response_data['Sales']['Upper date limit'])
        self.assertEqual(2, len(response_data['Sales']))


class TestSales(unittest.TestCase):

    def test_valid_dates(self):
        date_from = '2009-01-01'
        date_to = '2009-01-10'
        response = requests.get(BASE + '/sales/{}/{}'.format(date_from, date_to))
        status_code = response.status_code
        self.assertEqual(200, status_code)

    def test_one_date(self):
        date = '2009-01-03'
        response = requests.get(BASE + '/sales/{}/{}'.format(date, date))
        response_data = json.loads(response.text)
        status_code = response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(date, response_data['Sales']['1']['Date'])
        self.assertEqual(1, len(response_data['Sales']))

    def test_invalid_dates_non_chronological(self):
        date_from = '2020-01-03'
        date_to = '2020-01-01'
        response = requests.get(BASE + '/sales/{}/{}'.format(date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)

    def test_invalid_dates(self):
        date_from = 'sfs'
        date_to = '2020-01-01'
        response = requests.get(BASE + '/sales/{}/{}'.format(date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)

    def test_empty_dates(self):
        date_from = ''
        date_to = ''
        response = requests.get(BASE + '/sales/{}/{}'.format(date_from, date_to))
        status_code = response.status_code

        self.assertEqual(404, status_code)

    def test_invalid_dates_outside_limits(self):
        date_from = '2000-01-01'
        date_to = '2000-01-03'
        response = requests.get(BASE + '/sales/{}/{}'.format(date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)

    def test_invalid_dates_outside_range(self):
        date_from = '2000-01-01'
        date_to = '2020-01-03'
        response = requests.get(BASE + '/sales/{}/{}'.format(date_from, date_to))
        status_code = response.status_code

        self.assertEqual(400, status_code)
