<template>
  <div class="documentation">
    <!--    TODO: ogarnąć pierwszy kafelek + opis-->
    <div id="section-documentation" class="section">
      <h2>Documentation</h2>
      <p>This API service enables HTTP clients to make enquiries on the following datasets:</p>
      <ol>
        <li>historic exchange rates of PLN for foreign currencies</li>
        <ul>
          <li>USD</li>
          <li>EUR</li>
          <li>GBP</li>
        </ul>
        <li>CD shop sales history</li>
      </ol>
      <div id="section-general" class="section">
        <h4>General Information</h4>

        <p>Service reply is returned in <span class="code">JSON</span> format.</p>
        <p>Available historic data:</p>
        <div class="table">
          <!--          TODO: tabela przedziałów czasowych-->
        </div>
        <p>Single enquiry cannot cover a period longer than 365 days.</p>
      </div>

      <div id="section-table-of-contents" class="section">
        <h3>Table of contents</h3>
        <ul>
          <li><a href="#section-installation">Installation</a></li>
          <li><a href="#section-usage">Usage</a></li>
          <li><a href="#section-limits">Enquiry limits</a></li>
          <li><a href="#section-cache">Cache</a></li>
          <li><a href="#section-queries">Query examples</a></li>
          <li><a href="#section-errors">Error messages</a></li>
          <li><a href="#section-links">Links</a></li>
        </ul>
      </div>

      <div id="section-installation" class="section">
        <h2>Installation</h2>
        <p>Clone the repo and install dependencies:</p>
        <pre>
      <code>
        git clone https://github.com/limisie/skryptowe20.git
        cd skryptowe20
        git checkout L5_API
        pip install -r requirements.txt
      </code>
    </pre>
      </div>

      <div id="section-usage" class="section">
        <h2>Usage</h2>
        <p>Run the application with the command:</p>
        <code>python3 L5_API/app.py</code>
        <p>Then use one of the enquires:</p>
        <ul>
          <li>
            Latest value of exchange rate of currency <span class="code">{currencyCode}</span>
            <p><code>http://localhost:5000/rates/{currencyCode}</code></p>
          </li>
          <li>
            Date limits of exchange rate of currency <span class="code">{currencyCode}</span> in the database
            <p><code>http://localhost:5000/rates/{currencyCode}/limits</code></p>
          </li>
          <li>
            Exchange rate of currency <span class="code">{currencyCode}</span> published on <span
              class="code">{date}</span>
            (if the Interpolated field is <span class="code">true</span> the exchange
            rate is interpolated from nearest previous historic exchange rate)
            <p><code>http://localhost:5000/rates/{currencyCode}/{date}</code></p>
          </li>
          <li>
            Exchange rate of currency <span class="code">{currencyCode}</span> published from
            <span class="code">{startDate}</span> to <span class="code">{endDate}</span> (if the Interpolated field is
            <span class="code">true</span> the exchange rate is interpolated from nearest previous historic
            exchange rate)
            <p><code>http://localhost:5000/rates/{currencyCode}/{startDate}/{endDate}</code></p>
          </li>
          <li>
            Date limits of sales in the database
            <p><code>http://localhost:5000/sales/limits</code></p>
          </li>
          <li>
            Total sales in USD and PLN on <span class="code">{date}</span>
            <p><code>http://localhost:5000/sales/{date}</code></p>
          </li>
          <li>
            Total sales from <span class="code">{startDate}</span> to <span class="code">{endDate}</span>
            <p><code>http://localhost:5000/sales/{startDate}/{endDate}</code></p>
          </li>
        </ul>

        <h4>Query string parameters</h4>
        <ul>
          <li><span class="code">{currencyCode}</span> – a three- letter currency code (ISO 4217 standard)</li>
          <li><span class="code">{date}</span>, <span class="code">{startDate}</span>,
            <span class="code">{endDate}</span> – a date in the YYYY-MM-dd format (ISO 8601 standard)
          </li>
        </ul>
      </div>

      <div id="section-limits" class="section">
        <h2>Limits</h2>
        <p>There are limit for requests per user:</p>
        <ul>
          <li>1 per second</li>
        </ul>
        <p>and limits overall:</p>
        <ul>
          <li>100 per hour</li>
          <li>1000 per day</li>
        </ul>
      </div>

      <div id="section-cache" class="section">
        <h2>Cache</h2>
        <p>There are two cache instances that collect data of previous enquires. One for rates and one for sales data.
          Cache is refreshed every 24 hours.</p>
      </div>

      <div id="section-queries" class="section">
        <h2>Query examples</h2>
        <ul>
          <li>
            Latest value of USD
            <p><code>http://localhost:5000/rates/usd</code></p>
            <pre>
          <code>
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
          </code>
        </pre>
          </li>

          <li>
            Date limits of exchange rate of USD in the database
            <p><code>http://localhost:5000/rates/usd/limits</code></p>
            <pre>
          <code>
            {
              "Currency Code": "USD",
              "Limits": {
                "Lower date limit": "2009-01-01",
                "Upper date limit": "2021-01-19"
              }
            }
          </code>
        </pre>
          </li>

          <li>
            Exchange rate of currency EUR published from 2020-01-01 to 2020-01-02
            <p><code>http://localhost:5000/rates/eur/2020-01-01/2020-01-02</code></p>
            <pre>
          <code>
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
          </code>
        </pre>
          </li>

          <li>
            Total sales in USD and PLN on 2013-01-28
            <p><code>http://localhost:5000/sales/2013-01-28</code></p>
            <pre>
          <code>
            {
              "Sales": {
                "1": {
                  "Date": "2013-01-28",
                  "PLN Total": 12.3,
                  "USD Total": 3.96
                }
              }
            }
          </code>
        </pre>
          </li>

          <li>
            Date limits of sales in the database
            <p><code>http://localhost:5000/sales/limits</code></p>
            <pre>
          <code>
            {
              "Sales": {
                "Lower date limit": "2009-01-01",
                "Upper date limit": "2013-12-22"
              }
            }
          </code>
        </pre>
          </li>
        </ul>
      </div>

      <div id="section-errors" class="section">
        <h2>Error messages</h2>
        <p>In the case of enquiry for an invalid currency, <span
            class="code">404 - Currency Code not found is returned</span></p>
        <p>In the case of incorrect format of dates, the service returns <span class="code">400 BadRequest - Wrong format of dates - should be 0000-00-00</span>
          message</p>
        <p>In the case of incorrectly formulated dates, the service returns <span class="code">400 BadRequest - Invalid date range - endDate is before startDate</span>
          message or <span class="code">400 BadRequest - Invalid date range - date outside the database limit</span>
          if the
          dates are outside the limit</p>
        <p>In the case of an enquiry covering more than 365 days, the service returns the message <span class="code">400 BadRequest - Limit of 365 days has been exceeded</span>
        </p>
      </div>

      <div id="section-links" class="section">
        <h2>Links</h2>
        <h4>Dependencies</h4>
        <ul>
          <li><a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a></li>
          <li><a href="https://flask-restful.readthedocs.io/en/latest/">FlaskRESTful</a></li>
          <li><a href="https://flask-limiter.readthedocs.io/en/stable/">FlaskLimiter</a></li>
        </ul>
        <h4>Sources</h4>
        <ul>
          <li><a href="http://api.nbp.pl">NBP API</a></li>
          <li><a href="https://github.com/lerocha/chinook-database">Chinook Database</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Base',
}
</script>

<style scoped>

h1 {
  margin: 0;
}

code {
  display: block;
  padding: 10px;
  background-color: #fafafa;
  border-radius: 10px;
  border-style: none;
  overflow: auto;
}

.code {
  padding: 5px;
  background-color: #fafafa;
  border-radius: 10px;
  border-style: none;
  font-family: monospace;
}
</style>