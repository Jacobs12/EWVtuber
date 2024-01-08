"""
Author: wolffy
Date: 2023-10-11 17:09:13
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-17 18:35:33
FilePath: /EWVtuber/Command/command.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved.
"""

from Audio.audio import AudioManager
from Session.chatglm_session import ChatglmSession
from Platform.bilibili_livedanmaku import bilibiliDanmaku
from Session.langchain_session import  LangchainSession
from Utils import log
import vtuber


class CommandManager(object):
    # 音频管理器
    audio_manager: AudioManager
    # 会话管理器，主要用于与AI通信
    session_manager: ChatglmSession

    def __init__(self) -> None:
        # self.audio_manager = audio
        # self.session_manager = session
        pass

    def check_cmd(self, cmd: str = '') -> bool:
        log.add(log='cmd命令：' + cmd)
        #     恢复播放音频
        if cmd == '--play':
            self.audio_play()
        #     暂停播放音频
        elif cmd == '--pause':
            self.audio_pause()
        #     输出帮助信息
        elif cmd == '--help':
            self.help_prompt()
        #     输出试音音频
        elif cmd == '--test':
            player = vtuber.audio_player()
            player.test()
        #     停止播放音频
        elif cmd == '--stop':
            self.play_stop()
        #     登录第三方平台
        elif cmd == '--login':
            select = str(input('请选择登录的平台：\n  1.哔哩哔哩\n  2.抖音\n  3.快手\n>> '))
            if select == '1':
                # 登录哔哩哔哩
                self.start_bilibili_server()
            elif select == '2':
                # 登录抖音平台
                print('敬请期待哦~')
            elif select == '3':
                # 登录快手平台
                print('敬请期待哦~')
            else:
                print('无效的参数')
        elif cmd == '--ask':
            select = str(input(
                '本模式下可以在控制台与AI进行问答互动\n请选择问答模式：\n  1.普通问答模式\n  2.本地知识库问答模式\n>> '))
            if select == '1':
                # 进入普通问答模式
                selection = str(input('请选择服务器：\n  1.chatglm\n  2.langchain\n>> '))
                if selection == '1':
                    session = ChatglmSession()
                    result = session.ask(question=response,is_speak=False)
                elif selection == '2':
                    session = LangchainSession()
                    session.get_llm_ready()
                print(result)
            elif select == '2':
                # 进入知识库问答模式
                session = LangchainSession()
                session.get_knowledge_ready()
        elif cmd == '--live':
            select = str(
                input('您已进入直播模式，请确保开启voicemeeter\n请选择直播平台：\n  1.哔哩哔哩\n  2.抖音\n  3.快手\n>> '))
            if select == '1':
                self.live_bilibili_select()
            elif select == '2':
                # 登录抖音平台
                print('敬请期待哦~')
            elif select == '3':
                # 登录快手平台
                print('敬请期待哦~')
            else:
                print('无效的参数')

        if cmd == 'q' or cmd == 'quit' or cmd == 'exit' or 'app.py' in cmd or cmd == 'exit()' or '.py' in cmd:
            return True
        else:
            return False

    def check_audio_cmd(self, cmd: str = '', audio_manager: AudioManager = AudioManager()):
        # if cmd == 'play':
        #     self.audio_play()
        # elif cmd == 'pause':
        #     self.audio_pause()
        print('')

    """================================直播控制部分========================================"""

    def live_bilibili_select(self):
        select = str(input(
            '本模式下可以在第三方直播平台与AI进行弹幕问答互动\n请选择问答模式：\n  1.普通问答模式\n  2.本地知识库问答模式\n>> '))
        if select == '1':
            print('已进入哔哩哔哩普通直播问答模式，请确保开启voicemeeter\n')
            self.start_bilibili_server(session_type='chatglm')
            # 进入普通问答模式
            print('已进入哔哩哔哩普通直播问答模式，请确保开启voicemeeter\n')

        elif select == '2':
            # 进入知识库问答模式
            print('已进入哔哩哔哩本地知识库直播问答模式，请确保开启voicemeeter\n')  
            self.start_bilibili_server(session_type='langchain')
    def live_bilibili_normal(self,session_type:str = ''):
        self.start_bilibili_server(session_type=session_type)

    def start_bilibili_server(self,session_type:str = ''):
        bilibili_manager = bilibiliDanmaku()
        bilibili_manager.audio_manager = self.audio_manager
        bilibili_manager.session = session_type
        bilibili_manager.session_type = session_type
        bilibili_manager.langchain_session = LangchainSession()
        bilibili_manager.start_server()

    """================================音频控制部分====================================="""

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
        file = open('Config/commond.txt', encoding='utf-8')
        text = file.read()
        file.close()
        print(text)
