import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')
from langbly import Langbly
class chat_api:
    def send_message(message:str):
        trans = Langbly(api_key="PN4oc9vZk1zMXaoJsMTyJE")
        result = trans.translate(
            text=message,
            target="en"
        )
        return [result.source,result.text]



