from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import time

from L5_API.constants import DATE_FORMAT, CACHE_TIMEOUT


class Cache(ABC):
    time_to_refresh = CACHE_TIMEOUT
    data = {}

    def __init__(self):
        self.start = time.time()
        self.empty_cache = {}

    def refresh(self):
        if time.time() - self.start > self.time_to_refresh:
            self.data = self.empty_cache
            self.start = time.time()

    def is_cached_time_frame(self, date_from, date_to, code=''):
        date_from_obj = datetime.strptime(date_from, DATE_FORMAT)
        date_to_obj = datetime.strptime(date_to, DATE_FORMAT)
        temp_date_obj = date_from_obj

        while temp_date_obj <= date_to_obj:
            if not self.is_cached(temp_date_obj.strftime(DATE_FORMAT), code):
                return False
            temp_date_obj += timedelta(days=1)

        return True

    @abstractmethod
    def is_cached(self, date, code=''):
        pass

    @abstractmethod
    def get_cached(self, date_from, date_to, code=''):
        pass

    @abstractmethod
    def cache(self, data, code=''):
        pass


class RatesCache(Cache):
    data = {'USD': {}, 'EUR': {}, 'GBP': {}}

    def __init__(self):
        super().__init__()
        self.empty_cache = {'USD': {}, 'EUR': {}, 'GBP': {}}

    def is_cached(self, date, code=''):
        return date in self.data[code.upper()]

    def get_cached(self, date_from, date_to, code=''):
        data = []
        temp_date_obj = datetime.strptime(date_from, DATE_FORMAT)
        date_to_obj = datetime.strptime(date_to, DATE_FORMAT)

        while temp_date_obj <= date_to_obj:
            date = temp_date_obj.strftime(DATE_FORMAT)
            data.append({"date": date,
                         "rate": self.data[code.upper()][date][0],
                         "ipd": self.data[code.upper()][date][1]})
            temp_date_obj += timedelta(days=1)
        return data

    def cache(self, data, code=''):
        for d in data:
            date = d['date']
            rate = (d['rate'], d['ipd'])
            self.data[code.upper()][date] = rate


class SalesCache(Cache):
    def is_cached(self, date, code=''):
        return date in self.data

    def get_cached(self, date_from, date_to, code=''):
        data = []
        temp_date_obj = datetime.strptime(date_from, DATE_FORMAT)
        date_to_obj = datetime.strptime(date_to, DATE_FORMAT)

        while temp_date_obj <= date_to_obj:
            date = temp_date_obj.strftime(DATE_FORMAT)
            data.append({"date": date,
                         "total_usd": self.data[date][0],
                         "total_pln": self.data[date][1]})
            temp_date_obj += timedelta(days=1)
        return data

    def cache(self, data, code=''):
        for d in data:
            date = d['date']
            sale = (d['total_usd'], d['total_pln'])
            self.data[date] = sale
