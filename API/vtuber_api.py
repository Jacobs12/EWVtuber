"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""


def langchain_host() -> str:
    host = 'http://172.23.0.191:7866'
    return host


def shuziren_script_lists() -> str:
    url = 'http://172.23.0.191:10010/get_script_lists'
    return url


def shuziren_script_insert() -> str:
    url = 'http://172.23.0.191:10010/insert_script'
    return url
