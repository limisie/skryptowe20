import requests
from datetime import datetime, timedelta
from matplotlib import cycler, ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

MAX_TRIES = 10
MAX_TIME_FRAME = 366
PLOT_SIZE_X = 10
PLOT_SIZE_Y = 5
PLOT_LEFT_POS = 0.1
PLOT_BOTTOM_POS = 0.2
PLOT_MARGIN = 0.01
PLOT_TICKS_DAY_INTERVAL = 10
PLOT_TICKS_MINOR_X_INTERVAL = 180
PLOT_TICKS_Y_INTERVAL = 0.1
PLOT_TICKS_MINOR_Y_INTERVAL = 0.01
PLOT_GRID_LW = 0.25
PLOT_SAVE = False


def _url(path):
    return 'http://api.nbp.pl/api/exchangerates' + path


def currency_rates_and_dates_time_frame(currency_code, date_from, date_to):
    rates = []
    dates = []

    table = _get_table(currency_code)
    if not _are_dates(date_from, date_to) or not table:
        return rates, dates

    time_frames = _split_time_frame(date_from, date_to)

    for frame in time_frames:
        frame_dates = []
        frame_rates = []
        date_from, date_to = frame
        request = _get_rates_request(currency_code, table, date_from, date_to)

        if request.status_code == 200:
            data = request.json()['rates']
            n = len(data)

            for i in range(n):
                frame_rates.append(float(data[i]['mid']))
                frame_dates.append(data[i]['effectiveDate'])

        if not frame_dates or frame_dates[0] != date_from:
            frame_rates.insert(0, _currency_get_last_known_rate(currency_code, table, date_from))
            frame_dates.insert(0, date_from)

        if date_from != date_to and frame_dates[-1] != date_to:
            frame_rates.append(_currency_get_last_known_rate(currency_code, table, date_to))
            frame_dates.append(date_to)

        _fill_in_missing_rates(frame_rates, frame_dates)

        rates += frame_rates
        dates += frame_dates

    return rates, dates


def currency_rates_and_dates_from_last_days(currency_code, days):
    if not isinstance(days, int):
        return [], []

    date_from = (datetime.today() - timedelta(days=days - 1)).strftime('%Y-%m-%d')
    date_to = datetime.today().strftime('%Y-%m-%d')

    rates, dates = currency_rates_and_dates_time_frame(currency_code, date_from, date_to)

    return rates, dates


def _currency_get_last_known_rate(currency_code, table, date):
    rate = 0.0
    date = datetime.strptime(date, '%Y-%m-%d')
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

    date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
    date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
    temp_date_obj = date_from_obj

    while temp_date_obj <= date_to_obj:
        new_from = temp_date_obj
        new_to = new_from + timedelta(days=MAX_TIME_FRAME)

        if new_to > date_to_obj:
            new_to = date_to_obj

        date_frames.append((new_from.strftime('%Y-%m-%d'), new_to.strftime('%Y-%m-%d')))
        temp_date_obj = new_to + timedelta(days=1)

    return date_frames


def _fill_in_missing_rates(rates, dates):
    first_day = datetime.strptime(dates[0], '%Y-%m-%d')
    last_day = datetime.strptime(dates[len(dates) - 1], '%Y-%m-%d')
    delta = (last_day - first_day).days

    for i in range(delta):
        date = (first_day + timedelta(days=i)).strftime('%Y-%m-%d')

        if dates[i] != date:
            dates.insert(i, date)
            rates.insert(i, rates[i - 1])

    return rates, dates


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
        datetime.strptime(date_from, '%Y-%m-%d')
        datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        return False

    if date_from > date_to:
        return False

    return True


def plot(currencies, days):
    colors = cycler('color', ['goldenrod', 'lightsteelblue', 'olive', 'cadetblue'])
    plt.rc('axes', prop_cycle=colors)

    fig, ax = plt.subplots(figsize=(PLOT_SIZE_X, PLOT_SIZE_Y))
    plt.subplots_adjust(left=PLOT_LEFT_POS, bottom=PLOT_BOTTOM_POS)
    plt.margins(x=PLOT_MARGIN)

    x_min = '9999-99-99'
    x_max = '0000-00-00'
    y_ticks = {}

    for currency in currencies:
        rates, rate_dates = currency_rates_and_dates_from_last_days(currency, days)
        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in rate_dates]
        code = currency

        if dates and rates:
            plt.plot(dates, rates, label=code)
            y_ticks[currency] = rates[0]

            if rate_dates[0] < x_min:
                x_min = rate_dates[0]
            if rate_dates[-1] > x_max:
                x_max = rate_dates[-1]

    y_min = min(y_ticks.items(), key=lambda x: x[1])
    y_max = max(y_ticks.items(), key=lambda x: x[1])
    delta_y = y_max[1] - y_min[1]

    plt.title("Kursy średnie walut {} w dniach od {} do {}".format(
        ', '.join([str(code) for code in currencies]),
        x_min,
        x_max))
    plt.xlabel("data")
    plt.ylabel("kurs średni")

    delta_days = (datetime.strptime(x_max, '%Y-%m-%d') - datetime.strptime(x_min, '%Y-%m-%d')).days

    legend = plt.legend(loc='best')
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('white')
    plt.grid(axis='y', lw=PLOT_GRID_LW)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=delta_days // min(PLOT_TICKS_DAY_INTERVAL, delta_days)))
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=delta_days // min(PLOT_TICKS_MINOR_X_INTERVAL, delta_days)))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(PLOT_TICKS_Y_INTERVAL))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(PLOT_TICKS_MINOR_Y_INTERVAL))
    fig.autofmt_xdate()

    plt.show()
    if PLOT_SAVE:
        plt.savefig('rates.svg')
