import requests
from datetime import datetime, timedelta

from L5_API.constants import DATE_FORMAT, MAX_TRIES, DATA_LIMIT


def _url(path):
    return 'http://api.nbp.pl/api/exchangerates' + path


def currency_rates_dates_interpolated_time_frame(currency_code, date_from, date_to):
    rates = []
    dates = []
    interpolated = []

    table = _get_table(currency_code)
    if not _are_dates(date_from, date_to) or not table:
        return rates, dates

    time_frames = _split_time_frame(date_from, date_to)

    for frame in time_frames:
        frame_dates = []
        frame_rates = []
        frame_interpolated = []
        date_from, date_to = frame
        request = _get_rates_request(currency_code, table, date_from, date_to)

        if request.status_code == 200:
            data = request.json()['rates']
            n = len(data)

            for i in range(n):
                frame_rates.append(float(data[i]['mid']))
                frame_dates.append(data[i]['effectiveDate'])
                frame_interpolated.append(0)

        if not frame_dates or frame_dates[0] != date_from:
            frame_rates.insert(0, _currency_get_last_known_rate(currency_code, table, date_from))
            frame_dates.insert(0, date_from)
            frame_interpolated.insert(0, 1)

        if date_from != date_to and frame_dates[-1] != date_to:
            frame_rates.append(_currency_get_last_known_rate(currency_code, table, date_to))
            frame_dates.append(date_to)
            frame_interpolated.append(1)

        _fill_in_missing_rates(frame_rates, frame_dates, frame_interpolated)

        rates += frame_rates
        dates += frame_dates
        interpolated += frame_interpolated

    return rates, dates, interpolated


def currency_rates_dates_interpolated(currency_code, days):
    date_from = (datetime.today() - timedelta(days=days)).strftime(DATE_FORMAT)
    date_to = datetime.today().strftime(DATE_FORMAT)

    rates, dates, interpolated = currency_rates_dates_interpolated_time_frame(currency_code, date_from, date_to)

    return rates, dates, interpolated


def _currency_get_last_known_rate(currency_code, table, date):
    rate = 0.0
    date = datetime.strptime(date, DATE_FORMAT)
    request_code = 0
    tries_left = MAX_TRIES

    while request_code != 200 and tries_left > 0:
        request = _get_rates_request(currency_code, table, date.date(), date.date())
        request_code = request.status_code

        if request_code == 200:
            rate = request.json()['rates'][0]['mid']

        tries_left -= 1
        date = date - timedelta(days=1)

    return rate


def _split_time_frame(date_from, date_to):
    date_frames = []

    date_from_obj = datetime.strptime(date_from, DATE_FORMAT)
    date_to_obj = datetime.strptime(date_to, DATE_FORMAT)
    temp_date_obj = date_from_obj

    while temp_date_obj <= date_to_obj:
        new_from = temp_date_obj
        new_to = new_from + timedelta(days=DATA_LIMIT)

        if new_to > date_to_obj:
            new_to = date_to_obj

        date_frames.append((new_from.strftime(DATE_FORMAT), new_to.strftime(DATE_FORMAT)))
        temp_date_obj = new_to + timedelta(days=1)

    return date_frames


def _fill_in_missing_rates(rates, dates, interpolated):
    first_day = datetime.strptime(dates[0], DATE_FORMAT)
    last_day = datetime.strptime(dates[len(dates) - 1], DATE_FORMAT)
    delta = (last_day - first_day).days

    for i in range(delta):
        date = (first_day + timedelta(days=i)).strftime(DATE_FORMAT)

        if dates[i] != date:
            dates.insert(i, date)
            rates.insert(i, rates[i - 1])
            interpolated.insert(i, 1)

    return rates, dates, interpolated


def _get_rates_request(currency_code, table, date_from, date_to):
    url = _url("/rates/{}/{}/{}/{}".format(
        table,
        currency_code,
        date_from,
        date_to
    ))
    return requests.get(url)


def _get_table(currency_code):
    for table in ['A', 'B']:
        if _check_table(currency_code, table):
            return table
    return ''


def _check_table(currency_code, table):
    url = _url("/tables/{}".format(table))
    response = requests.get(url).json()

    for rate in response[0]['rates']:
        if rate['code'] == currency_code:
            return True

    return False


def _are_dates(date_from, date_to):
    try:
        datetime.strptime(date_from, DATE_FORMAT)
        datetime.strptime(date_to, DATE_FORMAT)
    except ValueError:
        return False

    return date_from <= date_to
