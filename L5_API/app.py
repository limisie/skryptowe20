from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask_restful import Api
from constants import DAY_LIMIT, HOUR_LIMIT, USER_LIMIT
from flask_cors import CORS
import views

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
limiter = Limiter(app,
                  key_func=get_remote_address,
                  default_limits=[USER_LIMIT],
                  application_limits=[DAY_LIMIT, HOUR_LIMIT])

app.add_url_rule('/rates/<code>', view_func=views.get_last_rate)
app.add_url_rule('/rates/<code>/limits', view_func=views.get_rates_limits)
app.add_url_rule('/rates/<code>/<date>', view_func=views.get_rate)
app.add_url_rule('/rates/<code>/<date_from>/<date_to>', view_func=views.get_rates)
app.add_url_rule('/sales/<date>', view_func=views.get_sale)
app.add_url_rule('/sales/<date_from>/<date_to>', view_func=views.get_sales)
app.add_url_rule('/sales/limits', view_func=views.get_sales_limits)


if __name__ == "__main__":
    app.run(debug=True)
