import time

import requests
import json

import API.vtuber_api
from EWSpeech.speech import Speaker
import log
from Session.session import Session


class LangchainSession(Session):
    def __init__(self):
        super().__init__()

    def get_llm_ready(self):
        print('已经入llm普通问答模式：')
        print('请输入你想问的问题：')
        history = []
        while True:
            question = str(input('>> '))
            if question == 'q':
                break
            response, record = self.chat_normal(question=question, history=history)
            history.extend(record)
            print(history)

    def chat_normal(self, question: str = '', history: list = None) -> (str, list):
        response = ''
        try:
            url = f"{self.host()}/chat/chat"
            headers = self.headers()

            if history is None:
                history = []
            question = self.pre_question() + question
            print(question)
            params = {
                "query": question,
                "history": history,
                "stream": False,
                "model_name": "chatglm2-6b",
                "temperature": 0.7,
                "prompt_name": "llm_chat"
            }
            data = json.dumps(params)
            print(params)
            response_data = requests.post(url=url, data=data, headers=headers)

            response = response_data.text
            log.add(f'user:{question}\n   AI:{response}')
            history = [
                {
                    "role": "user",
                    "content": question
                },
                {
                    "role": "assistant",
                    "content": response
                }
            ]
            print(response)
        except:
            print('未连接服务器')
        # if is_speak:
        #     speaker = Speaker()
        #     speaker.speak(response)

        return response, history

    def get_knowledge_ready(self):
        knowledge_lists = self.get_knowledge_lists()
        prompt = self.get_knowledge_prompt(knowledge_lists)
        print(prompt)
        selection = str(input('>> '))
        knowledge_base_name = knowledge_lists[int(selection) - 1]
        print('请输入你想问的问题：')
        history = []
        while True:
            question = str(input('>> '))
            if question == 'q':
                break
            response, record = self.chat_knowledge(knowledge_base_name=knowledge_base_name, question=question,
                                                   history=history)
            history.extend(record)
            print(history)

    def get_knowledge_prompt(self, knowledge_lists: list = None):
        print('已进入知识库问答模式，请选择知识库：')
        prompt = ''
        count = 0
        for item in knowledge_lists:
            count += 1
            if count >= len(knowledge_lists):
                prompt = f'{prompt}  {count}.{item}'
            else:
                prompt = f'{prompt}  {count}.{item}\n'
        return prompt

    def host(self) -> str:
        super().host()
        host = API.vtuber_api.langchain_host()
        return host

    # '''============================chat===================================='''

    def chat_knowledge(self, knowledge_base_name: str = '', question: str = '', history: list = None) -> (str, list):
        # time.sleep(5)
        # return '你好呀',[]
        if knowledge_base_name is None or knowledge_base_name == '':
            knowledge_base_name = 'ewangcom'
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
        log.add(f'knowledge_base_name:{knowledge_base_name}\n   user:{question}\n   AI:{answer}')
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
        return answer, history

    # '''============================Knowledge Base Management===================================='''

    # 获取知识库列表
    def get_knowledge_lists(self) -> list:
        try:
            url = f'{self.host()}/knowledge_base/list_knowledge_bases'
            headers = self.headers()
            response_data = requests.get(url=url)
            response = response_data.text
            dic = json.loads(response)
            result: list = dic['data']
            return result
        except:
            print('无法获取知识库列表')
            return ['无法获取知识库列表']


if __name__ == '__main__':
    session = LangchainSession()
    session.get_knowledge_lists()
