'''
Author: wolffy
Date: 2023-10-16 16:55:56
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-18 14:56:00
FilePath: /EWVtuber/Session/chatglm_session.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved. 
'''
import requests
import json
from EWSpeech.speech import Speaker


class ChatglmSession(object):

    def ask(self, question: str = '',is_speak:bool = False) -> str:
        url = "http://172.23.0.189:8000"
        headers = {"Content-Type": "application/json"}

        question = '你的名字是光线智能AI虚拟主播，请回答下面的问题：' + question
        params = {
            "prompt": question,
            "history": []
        }
        data = json.dumps(params)
        print(params)
        responseData = requests.post(url=url, data=data, headers=headers)

        responseDict = json.loads(responseData.text)

        response = responseDict['response']

        if is_speak:
            speaker = Speaker(response)
            speaker.speak(response)

        return response
