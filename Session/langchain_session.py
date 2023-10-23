import requests
import json
from EWSpeech.speech import Speaker
import log


class LangchainSession(object):
    def __init__(self):
        pass

    def ask(self, question: str = '',is_speak:bool = False) -> str:
        url = "http://172.23.0.191:7866/chat/chat"
        headers = {"Content-Type": "application/json"}

        question = '你的名字是光线智能AI虚拟主播，请回答下面的问题：' + question
        # params = {
        #     "query": question,
        #     "history": [
        #         {
        #             "role": "user",
        #             "content": "你的名字是光线智能AI虚拟主播，请不要回答敏感问题"
        #         },
        #         {
        #             "role": "assistant",
        #             "content": "好的，我会尽量遵守你的要求，光线智能AI虚拟主播。有任何需要帮助的问题，请随时提问。"
        #         }
        #     ],
        #     "stream": False,
        #     "model_name": "chatglm2-6b-int4",
        #     "temperature": 0.7,
        #     "prompt_name": "llm_chat"
        # }
        params = {
            "query": question,
            "history": [
            ],
            "stream": False,
            "model_name": "chatglm2-6b",
            "temperature": 0.7,
            "prompt_name": "llm_chat"
        }
        data = json.dumps(params)
        print(params)
        responseData = requests.post(url=url, data=data, headers=headers)

        response = responseData.text
        log.add(f'AI:{response}')
        if is_speak:
            speaker = Speaker(response)
            speaker.speak(response)

        return response