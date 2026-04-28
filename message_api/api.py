import requests
import pycountry
import sys
sys.stdout.reconfigure(encoding='utf-8')
from langbly import Langbly
class chat_api:
    def send_message(message:str):
        if message.isdigit() == True or message.isalnum() == False or message.isspace():
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


