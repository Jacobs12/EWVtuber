'''
Author: wolffy
Date: 2023-10-11 17:09:13
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-11 18:26:25
FilePath: /EWVtuber/Command/command.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved. 
'''

from Audio.audio import audioManager

class commandManager(object):
    def __init__(self) -> None:
        pass

    def check_cmd(self,cmd:str = '') -> bool:
        if cmd == 'q' or cmd == 'quit' or cmd == 'exit' or 'app.py' in cmd or cmd == 'exit()':
            return True
        else:
            return False
        
    def check_audio_cmd(self,cmd:str = '',audio_manager:audioManager = audioManager()):
        if cmd == 'play':
            postion = audio_manager.player.get_pos()
            if postion > 0:
                audio_manager.unpause()
            else:
                audio_manager.play()
        elif cmd == 'pause':
            audio_manager.pause()
        