'''
Author: wolffy
Date: 2023-10-18 14:02:35
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-18 15:46:09
FilePath: /EWVtuber/Platform/bilibili_livedanmaku.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved. 
'''
from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom

import log
from Session.chatglm_session import ChatglmSession
from EWSpeech.speech import Speaker
from Audio.audio import AudioManager
from bilibili_api.login import login_with_password, login_with_sms, send_sms, PhoneNumber, Check
from bilibili_api.user import get_self_info
from bilibili_api import settings
from bilibili_api import sync
from bilibili_api import login, user, sync
from  Session.langchain_session import LangchainSession

class bilibiliDanmaku(object):
    session: ChatglmSession = None
    audio_manager: AudioManager = None
    langchain_session:LangchainSession = None
    session_type:str = 'langchain'

    def __init__(self) -> None:
        pass

    def start_server(self):
        credential = self.login()
        # 自己直播间号
        ROOMID = 30923980
        # 凭证 根据回复弹幕的账号填写
        # credential = Credential(
        #     sessdata="",
        #     bili_jct=""
        # )
        # 监听直播间弹幕
        monitor = LiveDanmaku(ROOMID, credential=credential)
        # 用来发送弹幕
        sender = LiveRoom(ROOMID, credential=credential)
        # 自己的UID 可以手动填写也可以根据直播间号获取
        UID = sync(sender.get_room_info())["room_info"]["uid"]

        @monitor.on("DANMU_MSG")
        async def recv(event):
            # 发送者UID
            uid = event["data"]["info"][2][0]
            # 排除自己发送的弹幕
            # if uid == UID:
            #     return
            # 弹幕文本
            msg = event["data"]["info"][1]
            # if msg == "你好":
            #     # 发送弹幕
            #     await sender.send_danmaku(Danmaku("你好！"))
            response = ''
            if self.session_type == 'chatglm':
                if self.session == None:
                    self.session = ChatglmSession()
                response = self.session.ask(msg, is_speak=True)
            else:
                if self.langchain_session == None:
                    self.langchain_session = LangchainSession()
                response = self.langchain_session.ask(question=msg,is_speak=True)
            # response = self.session.ask(msg,is_speak=True)
            print(response)
            info = event["data"]["info"]
            log.add(f'来自哔哩哔哩：{info}')
            # log.add(f'接收到弹幕：')
            if '歌' in response:
                self.audio_manager.test()
                return
            speaker = Speaker(response)
            speaker.audio_manager = self.audio_manager
            speaker.speak(response)

            self.audio_manager.play(filename=speaker.output_path)

        # 启动监听
        sync(monitor.connect())

    def login(self):
        print("请登录：")
        # credential = login.login_with_qrcode_term() # 在终端扫描二维码登录
        credential = login.login_with_qrcode()  # 使用窗口显示二维码登录
        try:
            credential.raise_for_no_bili_jct()  # 判断是否成功
            credential.raise_for_no_sessdata()  # 判断是否成功
        except:
            print("登陆失败。。。")
            exit()
        print("欢迎，", sync(user.get_self_info(credential))['name'], "!")
        return credential

    def login_with_password(self):
        mode = int(input("""请选择登录方式：
        1. 密码登录
        2. 验证码登录
        请输入 1/2
        """))
        credential = None
        # 关闭自动打开 geetest 验证窗口
        settings.geetest_auto_open = False
        if mode == 1:
            # 密码登录
            username = input("请输入手机号/邮箱：")
            password = input("请输入密码：")
            print("正在登录。")
            c = login_with_password(username, password)
            if isinstance(c, Check):
                # 还需验证
                phone = print("需要进行验证。请考虑使用二维码登录")
                exit(1)
            else:
                credential = c
            print("登录成功")
        elif mode == 2:
            # 验证码登录
            phone = input("请输入手机号：")
            print("正在登录。")
            send_sms(PhoneNumber(phone, country="+86")) # 默认设置地区为中国大陆
            code = input("请输入验证码：")
            c = login_with_sms(PhoneNumber(phone, country="+86"), code)
            if isinstance(c, Check):
                # 还需验证
                phone = print("需要进行验证。请考虑使用二维码登录")
                exit(1)
            else:
                credential = c
            print("登录成功")
        else:
            print("请输入 1/2 ！")
            exit()

        if credential != None:
            name = sync(get_self_info(credential))['name']
            print(f"欢迎，{name}!")

