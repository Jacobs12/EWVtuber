'''
Author: wolffy
Date: 2023-10-11 16:42:53
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-11 18:03:45
FilePath: /EWVtuber/app.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved. 
'''

from Audio.audio import audioManager
from Command.command import commandManager

if __name__ == '__main__':

    audio_manager = audioManager()
    audio_manager.play(filename='Tmp/1.mp3')
    cmd_mananger = commandManager()

    while True:
        cmd = input('请输入命令:\n')
        is_break = cmd_mananger.check_cmd(cmd=str(cmd))
        if is_break:
            break
        cmd_mananger.check_audio_cmd(cmd=str(cmd),audio_manager=audio_manager)



