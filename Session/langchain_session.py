import requests
import json

import API.vtuber_api
from EWSpeech.speech import Speaker
import log
from Session.session import Session


class LangchainSession(Session):
    def __init__(self):
        super().__init__()

    def get_knowledge_ready(self):
        print('已进入知识库问答模式，请选择知识库：')
        knowledge_lists = self.get_knowledge_lists()
        prompt = ''
        count = 0
        for item in knowledge_lists:
            count += 1
            if count >= len(knowledge_lists):
                prompt = f'{prompt}  {count}.{item}'
            else:
                prompt = f'{prompt}  {count}.{item}\n'
        print(prompt)
        selection = str(input('>> '))
        knowledge_base_name = knowledge_lists[int(selection)-1]
        print('请输入你想问的问题：')
        history = []
        while True:
            question = str(input('>> '))
            if question == 'q':
                break
            record = self.chat_knowledge(knowledge_base_name=knowledge_base_name,question=question,history=history)
            history.extend(record)
            print(history)

    def ask(self, question: str = '', is_speak: bool = False) -> str:
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
        # print(params)
        responseData = requests.post(url=url, data=data, headers=headers)

        response = responseData.text
        log.add(f'AI:{response}')
        if is_speak:
            speaker = Speaker()
            speaker.speak(response)

        return response

    def host(self) -> str:
        super().host()
        host = API.vtuber_api.langchain_host()
        return host

    # '''============================chat===================================='''

    def chat_knowledge(self,knowledge_base_name:str = '',question:str = '',history:list = []) -> list:
        log.add(f'user:{question}')
        question = f'{self.pre_question()}{question}'
        url = f'{self.host()}/chat/knowledge_base_chat'
        headers = self.headers()
        parameters = {
                      "query": question,
                      "knowledge_base_name": knowledge_base_name,
                      "top_k": 3,
                      "score_threshold": 1,
                      "history": history,
                      "stream": False,
                      "model_name": "chatglm2-6b",
                      "temperature": 0.7,
                      "prompt_name": "knowledge_base_chat",
                      "local_doc_url": False
                    }
        data = json.dumps(parameters)
        response_data = requests.post(url=url, data=data, headers=headers)
        response = response_data.text
        dic = json.loads(response)
        answer = dic['answer']
        log.add(f'AI:{answer}')
        history = [
            {
                "role": "user",
                "content": question
            },
            {
                "role": "assistant",
                "content": answer
            }
        ]
        print(response)
        return history

    # '''============================Knowledge Base Management===================================='''

    # 获取知识库列表
    def get_knowledge_lists(self) -> list:
        url = f'{self.host()}/knowledge_base/list_knowledge_bases'
        headers = self.headers()
        response_data = requests.get(url=url)
        response = response_data.text
        dic = json.loads(response)
        result: list = dic['data']
        return result


if __name__ == '__main__':
    session = LangchainSession()
    session.get_knowledge_lists()
