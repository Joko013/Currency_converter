import redis
from tables import DataTables, SourceAPIError


class Converter(object):
    """ Currency converter object to encapsulate conversion and symbol decoding. """
    def __init__(self):
        self._dt = DataTables()

    def decode_symbol(self, symbol):
        """ Try and decode if currency [symbol] was provided. """

        self._symbol_data = self._dt.symbols
        try:
            return self._symbol_data[symbol]
        except KeyError:
            return symbol

    def convert_currency(self, amount, input_currency, output_currency=None):
        """ Convert [amount] in [input_currency] to [output_currency]
         or all currencies if [output_currency] is None. """

        try:
            self._currency_data = self._dt.exchange_rates

            self._input_currency = self.decode_symbol(input_currency)    # decode input curr symbol
            self._output_currency = self.decode_symbol(output_currency)  # decode output curr symbol

            self._amount = float(amount)

            # convert from input_currency to EUR
            self._to_eur = self._amount / self._currency_data["rates"][self._input_currency]

            # convert from EUR to output_currency
            if output_currency:
                to_output = round(self._to_eur * self._currency_data["rates"][self._output_currency], 2)
                self._dict_out = {self._output_currency: to_output}
            #  or all currencies
            else:
                to_output = [round(self._to_eur * rate, 2) for rate in self._currency_data["rates"].values()]
                currencies = [curr for curr in self._currency_data["rates"].keys()]
                self._dict_out = dict(zip(currencies, to_output))

            self.result = {
                "input": {"amount": self._amount, "currency": self._input_currency},
                "output": self._dict_out
                      }

            return self.result

        except KeyError:
            return {"Error": "[input_currency] or [output_currency] not found. Check the spelling of "
                    "supported currencies at https://www.exchangerate-api.com/supported-currencies."}

        except (ValueError, TypeError):
            return {"Error": "Please enter a valid [amount] (i.e. 13.37) to be converted."}

        except redis.ConnectionError:
            return {"Error": "Cannot connect to Redis server."}

        except SourceAPIError:
            return {"Error": "Cannot retrieve exchange rates from source, please try again later."}


