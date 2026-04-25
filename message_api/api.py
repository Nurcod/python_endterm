import requests
import pycountry
import sys
sys.stdout.reconfigure(encoding='utf-8')
from langbly import Langbly
url = "https://ws.detectlanguage.com/0.2/detect"
api_Key = "e4f5e7648bd2ebcc7108ed842f3ded50"
headers = {
    "Authorization": f"Bearer {api_Key}"
}
class chat_api:
    def send_message(message:str):
        data = {'q': message}
        response = requests.post(url,headers=headers,data=data).json()['data']['detections']
        response_code = [x['language'] for x in response if x['isReliable'] == True ]
        response = [pycountry.languages.get(alpha_2=x).name for x in response_code if pycountry.languages.get(alpha_2=x)]
        if response != []:
            trans = Langbly(api_key="PN4oc9vZk1zMXaoJsMTyJE")
            result = trans.translate(
                text=message,
                source=response_code,
                target="en"
            )
            return [response[0],result.text]
        return response



