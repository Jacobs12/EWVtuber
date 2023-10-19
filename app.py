"""
Author: wolffy
Date: 2023-10-11 16:42:53
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-18 14:27:36
FilePath: /EWVtuber/app.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved.
"""

from Audio.audio import audioManager
from Command.command import commandManager
import os
from EWSpeech.speech import Speaker
from Session.chatglm_session import ChatglmSession
from Platform.bilibili_livedanmaku import bilibiliDanmaku

if __name__ == '__main__':

    session = ChatglmSession()

    audio_manager = audioManager()

    # audio_manager.play(filename='Buffer\\Audio\\speech.wav')
    # audio_manager.play(filename='Tmp/1.mp3')
    cmd_mananger = commandManager(audio=audio_manager, session=session)
    cmd_mananger.audio_player = audio_manager
    cmd_mananger.session_manager = session
    bilibili_manager = bilibiliDanmaku()
    bilibili_manager.session = session
    bilibili_manager.audio_manager = audio_manager

    while True:
        cmd = input('>> ')
        history_cmd = cmd
        is_break = cmd_mananger.check_cmd(cmd=str(cmd))
        if is_break:
            break
        cmd_mananger.check_audio_cmd(cmd=str(cmd), audio_manager=audio_manager)

        if 'speak' in cmd:
            audio_manager.player.unload()
            # try:
            #     os.remove('Buffer\\Audio\\speech.wav')
            # except:
            #     print('')
            cmd = cmd.replace('speak', '')
            session.ask(question=cmd)
            print(session)
            audio_manager.play(filename='Buffer\\Audio\\speech.wav')
        if 'ask' in cmd:
            audio_manager.player.unload()
            # try:
            #   os.remove('Buffer\\Audio\\speech.wav')
            # except:
            #   print('')
            cmd = cmd.replace('ask', '')
            response = session.ask(question=cmd)
            print(response)
            audio_manager.play(filename='Buffer\\Audio\\speech.wav')


    def startbilibiliconnect():
        global bilibili_manager
        bilibili_manager.startServer()
