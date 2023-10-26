"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""

import requests
import json
import API.vtuber_api


class Session(object):
    def __init__(self):
        pass

    def pre_question(self) -> str:
        question = '你的名字是光线智能AI虚拟主播，不要回答敏感问题，请回答下面的问题：'
        return question

    def host(self) -> str:
        return ''

    def headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        return headers

    def parameters(self) -> dict:
        parameters = {}
        return parameters

    # 向AI发送post请求
    def start_request(self, msg: str = '') -> str:
        url = self.url()
        headers = self.headers()
        parameters = self.parameters()
        response_data = requests.post(url=url, headers=headers, data=parameters)
        response = response_data.text
        return response

    def send_to_ai(self, question: str = '') -> str:
        response = self.start_request()
        return response
