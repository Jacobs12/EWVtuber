import requests
import json
from Speech.speech import Speaker

class ChatglmSession(object):

    def ask(self,question:str = '') -> str:
        url = "http://172.23.0.189:8000"
        headers = {"Content-Type":"application/json"}

        params = {
            "prompt":question,
            "history":[]
        }
        data = json.dumps(params)
        print(params)
        responseData = requests.post(url=url,data=data,headers=headers)

        responseDict = json.loads(responseData.text)

        response = responseDict['response']

        speaker = Speaker(response)
        speaker.speak(response)

        return response