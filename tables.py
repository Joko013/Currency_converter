import requests
import json
from datetime import datetime, timedelta
from data_storage import RedisStorage


class DataTables(object):
    """ Object for working with currency exchange rates/symbols. """

    def __init__(self):
        self._RS = RedisStorage()

    def _get_exchange_rates(self):
        """ Get exchange rates from Redis server or ExchangeRate-API. """

        if not self._RS.get_data("exchange_rates"):
            url = 'https://v3.exchangerate-api.com/bulk/46b9b63b5c3949ad3cb209a1/EUR'
            self._response = requests.get(url)
            self._exchange_rates = self._response.json()   # {"result": "failed"}

            # in case source API does not return valid exchange rates raise error
            if self._exchange_rates["result"] == "success":
                # fresh data is available every hour before half
                expire_at = datetime.now().replace(microsecond=0, second=0, minute=30)+timedelta(hours=1)
                return self._RS.set_data("exchange_rates", self._exchange_rates, expire_at)
            else:
                raise SourceAPIError

        else:
            return self._RS.get_data("exchange_rates")

    @property
    def exchange_rates(self):
        return self._get_exchange_rates()

    def _get_symbols(self):
        """ Get currency symbols used for decoding input into currency codes. """

        if not self._RS.get_data("symbols"):
            with open("symbols_data.json", encoding="utf8") as f:
                self._symbol_data = json.load(f)
            return self._RS.set_data("symbols", self._symbol_data)
        else:
            return self._RS.get_data("symbols")

    @property
    def symbols(self):
        return self._get_symbols()


class SourceAPIError(Exception):
    """ Error to be raised when the application cannot connect to source API correctly. """
    def __init__(self):
        print(" Error when retrieving exchange rates from source API. ")

