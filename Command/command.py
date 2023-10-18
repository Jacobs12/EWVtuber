'''
Author: wolffy
Date: 2023-10-11 17:09:13
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-17 18:35:33
FilePath: /EWVtuber/Command/command.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved. 
'''

from Audio.audio import audioManager
from Session.chatglm_session import ChatglmSession
import os

class commandManager(object):
    # 音频管理器
    audio_manager : audioManager 
    # 会话管理器，主要用于与AI通信
    session_manager : ChatglmSession 
    def __init__(self,audio,session) -> None:
        self.audio_manager = audio
        self.session_manager = session

    def check_cmd(self,cmd:str = '') -> bool:
        if cmd == '--play':
            self.audio_play()
        elif cmd == '--pause':
            self.audio_pause()
        elif cmd == '--help':
            self.help_prompt()
        elif cmd == '--test':
            self.play_test()
        elif cmd == '--stop':
            self.play_stop()

        if cmd == 'q' or cmd == 'quit' or cmd == 'exit' or 'app.py' in cmd or cmd == 'exit()' or '.py' in cmd:
            return True
        else:
            return False
        
    def check_audio_cmd(self,cmd:str = '',audio_manager:audioManager = audioManager()):
        # if cmd == 'play':
        #     self.audio_play()
        # elif cmd == 'pause':
        #     self.audio_pause()
        print('')

    # 开始播放音频
    def audio_play(self):
        postion = self.audio_manager.player.get_pos()
        if postion > 0:
            self.audio_manager.unpause()
        else:
            self.audio_manager.play()

    # 暂停播放音频
    def audio_pause(self):
        self.audio_manager.player.pause()

    # 试音
    def play_test(self):
        try:
            self.audio_manager.player.unload()
        except:
            print('')
        self.audio_manager.play(filename='Tmp/1.mp3')
        print('AI：当前正在试音，输入 --stop以结束试音')

    # 结束播放音频
    def play_stop(self):
        self.audio_manager.player.stop()
        self.audio_manager.player.unload()
        print('AI：音频播放结束')
    
    # 输出帮助信息
    def help_prompt(self):
        file = open('Config/commond.txt',encoding='utf-8')
        text = file.read()
        file.close()
        print(text)
