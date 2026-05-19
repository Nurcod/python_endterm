import requests
import pycountry
import sys
import requests
sys.stdout.reconfigure(encoding='utf-8')
from langbly import Langbly
class chat_api:
    def send_message(message:str):
        message = message.strip()
        if message.isdigit() == True or message.isspace() == True:
            return []
        trans = Langbly(api_key="PN4oc9vZk1zMXaoJsMTyJE")
        result = trans.translate(
            text=message,
            target="en"
        )
        if len(result.source) == 2:
            lang = pycountry.languages.get(alpha_2=result.source)
        else:
            lang = pycountry.languages.get(alpha_3=result.source)
        return [lang.name,result.text]
    def fact():
        try:
            header = {'X-Api-Key':'dfLnshzKWamd3iafkkrdgvwO5GOF4ZE0w9TszdMM'}
            req = requests.get('https://api.api-ninjas.com/v1/facts',header,timeout=5).json()[0]['fact']
            if req:
                return req
            else:
                return 'timeout,server probably closed,try again'
        except Exception as e:
            return e+' please try again'
    def weather(message:str):
        try:
            params = {
        "q": message,
        "appid": 'ed7162f68bf288b22dfb288f988ea233',
        "units": "metric",
        "lang": "ru"
    }
            req = requests.get('https://api.openweathermap.org/data/2.5/weather',params=params,timeout=5).json()
            if req:
                weather = req['weather'][0]['main']
                temp = req['main']['temp']
                wind_speed = req['wind']['speed']
                wind_deg = req['wind']['deg']
                return [weather,temp,wind_speed,wind_deg]
            else:
                return 'timeout,server probably closed,try again'
        except Exception as e:
            return e+' try again'
    def joke():
        try:
            header = {'X-Api-Key':'dfLnshzKWamd3iafkkrdgvwO5GOF4ZE0w9TszdMM'}
            req = requests.get('https://api.api-ninjas.com/v1/jokes',header,timeout=5).json()[0]['joke']
            if req:
                return req
            else:
                return 'timeout,server probably closed,try again'
        except Exception as e:
            return e+' try again'