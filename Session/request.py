"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import requests

from Utils.threading import EWThread as Thread


class Request(object):
    response = None

    def get(self, url: str, headers=None, query=None, completion_handler=None,failed_handler=None):
        if query is None:
            query = {}
        if headers is None:
            headers = {}
        if url is None or len(url) == 0:
            print('url不合法')
            return

        def request_process():
            print(headers)
            self.response = requests.get(url=url, headers=headers,params=query).content

        def request_finished():
            print(self.response)
            if completion_handler is not None:
                completion_handler(self.response)

        thread = Thread()
        thread.start(process_handler=request_process, completion_handler=request_finished)

    def post(self, url: str, headers=None, query=None, parameters=None,completion_handler=None,failed_handler=None):
        if query is None:
            query = {}
        if headers is None:
            headers = {}
        if url is None or len(url) == 0:
            print('url不合法')
            return

        def request_process():
            print(headers)
            self.response = requests.post(url=url, headers=headers,params=query,data=parameters).content

        def request_finished():
            # print(self.response)
            if completion_handler is not None:
                completion_handler(self.response)

        thread = Thread()
        thread.start(process_handler=request_process, completion_handler=request_finished)
