from L5_API import db_app
from L5_API.cache import RatesCache, SalesCache
from L5_API.validators import is_code, validate_dates

ratesCache = RatesCache()
salesCache = SalesCache()


def get_rates(code, date_from, date_to):
    if not is_code(code):
        return '404 - Currency Code not found', 404

    are_dates_valid = validate_dates(date_from, date_to, code)
    if not are_dates_valid[0]:
        return are_dates_valid[1], are_dates_valid[2]

    if ratesCache.is_cached_time_frame(date_from, date_to, code):
        data = ratesCache.get_cached(date_from, date_to, code)
    else:
        data = db_app.get_rates_ipd(code, date_from, date_to)
        ratesCache.cache(data, code)

    ratesCache.refresh()

    return _rates_serializer(code, data)


def get_rate(code, date):
    return get_rates(code, date, date)


def get_last_rate(code):
    limit = db_app.get_rates_limits(code)[1]
    return get_rates(code, limit, limit)


def get_sales(date_from, date_to):
    are_dates_valid = validate_dates(date_from, date_to)
    if not are_dates_valid[0]:
        return are_dates_valid[1], are_dates_valid[2]

    if salesCache.is_cached_time_frame(date_from, date_to):
        data = salesCache.get_cached(date_from, date_to)
    else:
        data = db_app.get_sales(date_from, date_to)
        salesCache.cache(data)

    salesCache.refresh()

    return _sales_serializer(data)


def get_sale(date):
    return get_sales(date, date)


def get_rates_limits(code):
    if not is_code(code):
        return '404 - Currency Code not found', 404

    date_min, date_max = db_app.get_rates_limits(code)
    return {"Currency Code": code.upper(), "Limits": {"Lower date limit": date_min, "Upper date limit": date_max}}


def get_sales_limits():
    date_min, date_max = db_app.get_sales_limits()
    return {"Sales": {"Lower date limit": date_min, "Upper date limit": date_max}}


def _sales_serializer(data):
    output = {"Sales": []}
    for index, d in enumerate(data, start=1):
        output["Sales"].append({"Date": d["date"],
                                "USD Total": d["total_usd"],
                                "PLN Total": d["total_pln"]})
    return output


def _rates_serializer(code, data):
    output = {"Currency Code": code.upper(), "Rates": []}
    for d in data:
        output["Rates"].append({"Date": d["date"],
                                "Rate": d["rate"],
                                "Interpolated": d["ipd"]})
    return output
