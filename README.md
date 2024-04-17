# Rates & Sales API

This API service enables HTTP clients to make enquiries on the following datasets:

1. historic exchange rates of PLN for foreign currencies
    * USD
    * EUR
    * GBP
2. CD shop sales history

#### General Information

Service reply is returned in `JSON` format.

Available historic data:

| Data              | First entry   |  Last entry   |
| ----------------- | ------------- | ------------- |
| Sales | 2009-01-01 | 2013-12-22 |
| USD exchange rates | 2009-01-01 | 2021-01-19 |
| EUR exchange rates | 2009-01-01 | 2021-01-19 |
| GBP exchange rates | 2009-01-01 | 2021-01-19 |

Single enquirey cannot cover a period longer than 365 days.

---

### Table of contents

* [Installation](#Installation)
* [Usage](#Usage)
* [Enquiry limits](#Limits)
* [Cache](#Cache)
* [Query examples](#Query-examples)
* [Error messages](#Error-messages)
* [Links](#Links)

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/limisie/skryptowe20.git
cd skryptowe20
git checkout L5_API
pip install -r requirements.txt
```

## Usage

Run the application with the command:

```bash
python3 L5_API/app.py
```

Then use one of the enquires

#### Rates data

* Date limits of exchange rate of currency `{currencyCode}` in the database
    ```bash
    http://localhost:5000/rates/{currencyCode}/limits
    ```
* Latest value of exchange rate of currency `{currencyCode}`
    ```bash
    http://localhost:5000/rates/{currencyCode}
    ```
* Exchange rate of currency `{currencyCode}` published on `{date}`
  (if the `Interpolated` field is `true` the exchange rate is interpolated from nearest previous historic exchange rate)
    ```bash
    http://localhost:5000/rates/{currencyCode}/{date}
    ```  
* Exchange rate of currency `{currencyCode}` published from `{startDate}` to `{endDate}`
  (if the `Interpolated` field is `true` the exchange rate is interpolated from nearest previous historic exchange rate)
    ```bash
    http://localhost:5000/rates/{currencyCode}/{startDate}/{endDate}
    ```

#### Sales data

* Date limits of sales in the database
    ```bash
    http://localhost:5000/sales/limits
    ```
* Total sales in USD and PLN on `{date}`
    ```bash
    http://localhost:5000/sales/{date}
    ```  
* Total sales from `{startDate}` to `{endDate}`
    ```bash
    http://localhost:5000/sales/{startDate}/{endDate}
    ```

#### Query string parameters

* `{currencyCode}` – a three- letter currency code (ISO 4217 standard)
* `{date}`, `{startDate}`, `{endDate}` – a date in the YYYY-MM-dd format (ISO 8601 standard)

## Limits

There are limit for requests per user:

* 1 per second

and limits overall:

* 100 per hour
* 1000 per day

## Cache

There are two cache instances that collect data of previous enquires. One for rates and one for sales data. Cache is
refreshed every 24 hours.

## Query examples

* Date limits of exchange rate of USD in the database
    ```bash
    http://localhost:5000/rates/usd/limits
    ```
  ```text
  {
    "Currency Code": "USD", 
    "Limits": {
      "Lower date limit": "2009-01-01", 
      "Upper date limit": "2021-01-19"
    }
  }
  ```
  
* Latest value of USD
    ```bash
    http://localhost:5000/rates/usd
    ```
  ```text
  {
    "Currency Code": "usd", 
    "Rates": {
      "Rate": {
        "Date": "2020-12-18", 
        "Interpolated": false, 
        "Rate": 3.6322
      }
    }
  }
  ```
  
* Exchange rate of currency EUR published from 2020-01-01 to 2020-01-02
    ```bash
    http://localhost:5000/rates/eur/2020-01-01/2020-01-02
    ```
    ```text
    {
      "Currency Code": "EUR", 
      "Rates": {
        "1": {
          "Date": "2020-01-01", 
          "Interpolated": true, 
          "Rate": 4.2585
        }, 
        "2": {
          "Date": "2020-01-02", 
          "Interpolated": false, 
          "Rate": 4.2571
        }
      }
    }
    ```
  
* Date limits of sales in the database
    ```bash
    http://localhost:5000/sales/limits
    ```
    ```text
    {
      "Sales": {
        "Lower date limit": "2009-01-01", 
        "Upper date limit": "2013-12-22"
      }
    }
    ```
  
* Total sales in USD and PLN on 2013-01-28
    ```bash
    http://localhost:5000/sales/2013-01-28
    ```
    ```text
    {
      "Sales": {
        "1": {
          "Date": "2013-01-28", 
          "PLN Total": 12.3, 
          "USD Total": 3.96
        }
      }
    }
    ```

## Error messages

In the case of enquiry for an invalid currency, `404 - Currency Code not found` is returned

In the case of incorrect format of dates, the service
returns `400 BadRequest - Wrong format of dates - should be 0000-00-00` message

In the case of incorrectly formulated dates, the service
returns `400 BadRequest - Invalid date range - endDate is before startDate` message
or `400 BadRequest - Invalid date range - date outside the database limit` if the dates are outside the limit

In the case of an enquiry covering more than 365 days, the service returns the
message `400 BadRequest - Limit of 365 days has been exceeded`

## Links

#### Dependencies

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [FlaskRESTful](https://flask-restful.readthedocs.io/en/latest/)
* [FlaskLimiter](https://flask-limiter.readthedocs.io/en/stable/)

#### Sources

* [NBP API](http://api.nbp.pl)
* [Chinook Database](https://github.com/lerocha/chinook-database)
