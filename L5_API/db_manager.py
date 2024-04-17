import sqlite3
from L5_API.constants import DB_PATH


def _connect_db():
    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print('db_handler: connect_db ' + str(e))

    return conn


def _drop_rates_table():
    conn = _connect_db()
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE rates;""")

    conn.commit()
    conn.close()


def _create_rates_table():
    conn = _connect_db()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE rates (
                        RateDate data_type BLOB NOT NULL,
                        Rate data_type REAL NOT NULL,
                        Code data_type TEXT NOT NULL,
                        Interpolated BOOLEAN NOT NULL CHECK (Interpolated IN (0, 1)),
                        CONSTRAINT rates_pk PRIMARY KEY (RateDate, Code)
                   );""")

    conn.commit()
    conn.close()


def _get_invoices():
    conn = _connect_db()
    cursor = conn.cursor()
    data = []

    try:
        cursor.execute("""SELECT * FROM invoices;""")
        for inv in cursor.fetchall():
            data.append(inv)
    except sqlite3.Error as e:
        print('db_handler: get_invoices' + str(e))

    conn.close()
    return data


def _add_total_pln_sales_column():
    conn = _connect_db()
    cursor = conn.cursor()

    cursor.execute("""ALTER TABLE invoices ADD Total_pln NUMERIC(10,2) DEFAULT 0.00;""")

    conn.commit()
    conn.close()


def _add_total_pln_sales():
    conn = _connect_db()
    cursor = conn.cursor()
    dates = []
    rate = 0.0
    sale = 0.0

    try:
        cursor.execute("""SELECT InvoiceDate FROM invoices;""")
        for date in cursor.fetchall():
            dates.append(date[0][:10])
    except sqlite3.Error as e:
        print('db_handler: __add_total_pln_sales(): SELECT InvoiceDate FROM invoices ' + str(e))

    for date in dates:
        try:
            cursor.execute("""SELECT Rate FROM rates WHERE RateDate = '{}' AND Code = 'USD';""".format(date))
            rate = float(cursor.fetchone()[0])
        except sqlite3.Error as e:
            print('db_handler: __add_total_pln_sales() ' + str(e))

        try:
            cursor.execute("""SELECT Total FROM invoices 
                              WHERE InvoiceDate == '{}';""".format('{} 00:00:00'.format(date)))
            sale = float(cursor.fetchone()[0])
        except sqlite3.Error as e:
            print('db_handler: __add_total_pln_sales(): SELECT Total FROM invoices ' + str(e))

        try:
            cursor.execute("""UPDATE invoices SET Total_pln = {}
                              WHERE InvoiceDate == '{}';""".format(round(rate * sale, 2), '{} 00:00:00'.format(date)))
        except sqlite3.Error as e:
            print('db_handler: __add_total_pln_sales(): UPDATE invoices ' + str(e))

    conn.commit()
    conn.close()


def get_rates_dates_interpolated(currency_code, date_from, date_to):
    conn = _connect_db()
    cursor = conn.cursor()
    rates = []
    dates = []
    interpolated = []

    try:
        cursor.execute("""SELECT Rate, RateDate, Interpolated FROM rates
                            WHERE RateDate BETWEEN '{}' AND '{}'
                            AND Code = '{}';""".format(date_from, date_to, currency_code))
        for rate, date, ipd in cursor.fetchall():
            rates.append(float(rate))
            dates.append(date)
            interpolated.append(ipd)
    except sqlite3.Error as e:
        print('db_handler: get_rates' + str(e))

    conn.close()

    return rates, dates, interpolated


def get_rate_interpolated(currency_code, date):
    return get_rates_dates_interpolated(currency_code, date, date)


def get_sales_and_dates(date_from, date_to):
    conn = _connect_db()
    cursor = conn.cursor()

    sales_usd = []
    sales_pln = []
    dates = []

    try:
        cursor.execute("""SELECT SUM(Total), SUM(Total_pln), InvoiceDate FROM invoices
                                WHERE InvoiceDate BETWEEN '{}' AND '{}'
                                GROUP BY InvoiceDate""".format('{} 00:00:00'.format(date_from),
                                                               '{} 00:00:00'.format(date_to)))
        for sale_usd, sale_pln, date in cursor.fetchall():
            sales_usd.append(float(sale_usd))
            sales_pln.append(float(sale_pln))
            dates.append(date[:10])
    except sqlite3.Error as e:
        print('db_handler: get_sales' + str(e))

    conn.close()

    return sales_usd, sales_pln, dates


def get_sale_and_date(date):
    return get_sales_and_dates(date, date)


def delete_rate_entry(currency_code, date):
    conn = _connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""DELETE FROM rates
                            WHERE RateDate = '{}'
                            AND Code = '{}'""".format(date, currency_code))
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: delete_rate_entry ' + str(e))

    conn.close()


def add_rate_entries(currency_code, dates, rates, interpolated):
    conn = _connect_db()
    cursor = conn.cursor()

    try:
        for i in range(len(dates)):
            cursor.execute("""INSERT INTO rates VALUES (:RateDate, :Rate, :Code, :Interpolated)""",
                           {'RateDate': dates[i],
                            'Rate': rates[i],
                            'Code': currency_code,
                            'Interpolated': interpolated[i]})
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: add_rate_entries ' + str(e))

    conn.close()


def add_rate_entry(currency_code, date, rate, interpolated):
    return add_rate_entries(currency_code, [date], [rate], [interpolated])
