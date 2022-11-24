import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Не удалось перевести одинаковые валюты: {base}')

        try:
            keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.apilayer.com/currency_data/convert?to={keys[quote]}&from={keys[base]}&amount={amount}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

