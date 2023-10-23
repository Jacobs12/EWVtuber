"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""

import datetime
import os.path


def add(log: str):
    now = get_time()
    text = f'>> {now}\n   {log}\n'
    print(text)
    file_path = get_file_path()
    # print(file_path)
    fp = open(file_path,"a+")
    print(text, file=fp)
    fp.close()


def get_time():
    now = datetime.datetime.now()
    formatted = now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted


def get_dir_path() -> str:
    # 按天/小时建立日志文件夹
    now = datetime.datetime.now()
    day = now.strftime('%Y-%m-%d')
    hour = now.strftime('%Y-%m-%d_%H:00')
    base_path = f'Log/{day}/{hour}/'
    is_exist = os.path.exists(path=base_path)
    if not is_exist:
        os.makedirs(base_path)
    print(base_path)
    return base_path


def get_file_path() -> str:
    now = datetime.datetime.now()
    file_name = now.strftime('%Y-%m-%d_%H:%M:%S')
    base_path = get_dir_path()
    file_path = f'{base_path}{file_name}.txt'
    return file_path
