import json
import requests
from config import APILAYERTOKEN    



class APIException(Exception):
    pass

class Convertor:

    @staticmethod
    #Конвертор
    def get_price(base_currency, second_currency, amount):
        try:
            base_currency
        except KeyError:
            raise APIException(f"Валюта {base_currency} не найдена!")

        try:
            second_currency
        except KeyError:
            raise APIException(f"Валюта {second_currency} не найдена!")

        if base_currency == second_currency:
            raise APIException(f'Невозможно перевести одинаковые валюты {base_currency}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        #Формируем запрос
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={str(second_currency)}&from={str(base_currency)}&amount={str(amount)}"
        response = requests.request("GET", url, headers={"apikey": APILAYERTOKEN})
        status_code = response.status_code
        #лог кода ответа
        print(status_code)
        result = json.loads(response.text)
        #лог ответа
        print(result['query']['amount'], result['query']['from'], ' составит ',  result['result'], result['query']['to'])

        message =  f"По вашему запросу сообщаем, что {result['query']['amount']} {result['query']['from']}  =  {result['result']} {result['query']['to']}"
        return message
