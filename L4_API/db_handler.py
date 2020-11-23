from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DB_FILE = '/Users/limi/Desktop/INF/5 JS/L/skryptowe20/L4_API/sales.db'
PLOT_SIZE_X = 14
PLOT_SIZE_Y = 7
PLOT_LEFT_POS = 0.07
PLOT_RIGHT_POS = 0.93
PLOT_X_MARGINS = 0.01
PLOT_BAR_WIDTH = 0.9
PLOT_GRID_LW = 0.25

PLOT_SAVE = False


def connect_db():
    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)
    except sqlite3.Error as e:
        print('db_handler: connect_db ' + str(e))

    return conn


def create_rates_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE rates (
                        RateDate data_type BLOB,
                        Rate data_type REAL,
                        Code data_type TEXT
                   );""")

    conn.commit()
    conn.close()


def get_sales(date):
    conn = connect_db()
    cursor = conn.cursor()

    sales = []

    try:
        cursor.execute("""SELECT Total FROM invoices
                            WHERE InvoiceDate = '{} 00:00:00'""".format(date))
        sales = [float(x[0]) for x in cursor.fetchall()]
    except sqlite3.Error as e:
        print('db_handler: get_sales ' + str(e))

    conn.close()

    return sales


def get_total_sale(date):
    return sum(get_sales(date))


def get_rate(date, currency_code):
    conn = connect_db()
    cursor = conn.cursor()
    rate = 0.0

    try:
        cursor.execute("""SELECT Rate FROM rates
                            WHERE RateDate = '{}'
                            AND Code = '{}';""".format(date, currency_code))
        rate = float(cursor.fetchone()[0])
    except sqlite3.Error as e:
        print('db_handler: get_rate(' + date + ', ' + currency_code + ') ' + str(e))

    conn.close()

    return rate


def get_rates_and_dates(currency_code, date_from, date_to):
    conn = connect_db()
    cursor = conn.cursor()
    rates = []
    dates = []

    try:
        cursor.execute("""SELECT Rate, RateDate FROM rates
                            WHERE RateDate BETWEEN '{}' AND '{}'
                            AND Code = '{}';""".format(date_from, date_to, currency_code))
        for rate, date in cursor.fetchall():
            rates.append(float(rate))
            dates.append(date)
    except sqlite3.Error as e:
        print('db_handler: get_rates' + str(e))

    conn.close()

    return rates, dates


def get_sales_and_dates(date_from, date_to):
    conn = connect_db()
    cursor = conn.cursor()

    sales = []
    dates = []

    try:
        cursor.execute("""SELECT SUM(Total), InvoiceDate FROM invoices
                                WHERE InvoiceDate BETWEEN '{}' AND '{}'
                                GROUP BY InvoiceDate""".format('{} 00:00:00'.format(date_from),
                                                               '{} 00:00:00'.format(date_to)))
        for sale, date in cursor.fetchall():
            sales.append(float(sale))
            dates.append(date[:10])
    except sqlite3.Error as e:
        print('db_handler: get_sales' + str(e))

    conn.close()

    return sales, dates


def add_rate_entry(date, rate, currency_code):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO rates VALUES (:RateDate, :Rate, :Code)""",
                       {'RateDate': date, 'Rate': rate, 'Code': currency_code})
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: add_rate_entry ' + str(e))

    conn.close()


def delete_rate_entry(date, currency_code):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""DELETE FROM rates 
                            WHERE RateDate = '{}'
                            AND Code = '{}'""".format(date, currency_code))
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: delete_rate_entry ' + str(e))

    conn.close()


def add_rate_entries(dates, rates, currency_code):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        for i in range(len(dates)):
            cursor.execute("""INSERT INTO rates VALUES (:RateDate, :Rate, :Code)""",
                           {'RateDate': dates[i], 'Rate': rates[i], 'Code': currency_code})
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: add_rate_entries ' + str(e))

    conn.close()


def data_to_plot(currency_code, date_from, date_to):
    rates, dates = get_rates_and_dates(currency_code, date_from, date_to)
    sales, sale_dates = get_sales_and_dates(date_from, date_to)
    sales_usd = []
    sales_pln = []

    sale_index = 0

    for i in range(len(dates)):
        if sale_index < len(sales) and dates[i] == sale_dates[sale_index]:
            sales_usd.append(sales[sale_index])
            sales_pln.append(sales[sale_index] * rates[i])
            sale_index += 1
        else:
            sales_usd.append(0.0)
            sales_pln.append(0.0)

    return dates, sales_usd, sales_pln


def plot_sale_time_frame(currency_code, date_from, date_to):
    sale_dates, sales_usd, sales_pln = data_to_plot(currency_code, date_from, date_to)

    fig, ax = plt.subplots(figsize=(PLOT_SIZE_X, PLOT_SIZE_Y))
    plt.subplots_adjust(left=PLOT_LEFT_POS, right=PLOT_RIGHT_POS)

    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in sale_dates]
    plt.bar(dates, sales_pln, width=PLOT_BAR_WIDTH, label='PLN')
    plt.bar(dates, sales_usd, width=PLOT_BAR_WIDTH, label='USD')
    plt.margins(x=PLOT_X_MARGINS)

    plt.title("Sales in USD and PLN from {} to {}".format(date_from, date_to))
    plt.xlabel("date")
    plt.ylabel("sale")

    legend = plt.legend(frameon=1, loc='best')
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('white')
    plt.grid(axis='y', lw=PLOT_GRID_LW)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    plt.show()
    if PLOT_SAVE:
        plt.savefig('sales.svg')


if __name__ == '__main__':
    # create_rates_table()
    pass
