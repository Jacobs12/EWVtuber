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
import json
import os.path

from bilibili_api import Credential
from bilibili_api.live import LiveDanmaku, LiveRoom

from Utils import log
from Session.chatglm_session import ChatglmSession
from EWSpeech.speech import Speaker
from Audio.audio import AudioManager
from bilibili_api.login import login_with_password, login_with_sms, send_sms, PhoneNumber, Check
from bilibili_api.user import get_self_info
from bilibili_api import settings
from bilibili_api import login, user, sync
from  Session.langchain_session import LangchainSession
import pickle
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QThread,pyqtSignal,QObject
import threading

# self.thread = QThread()
#         w = Worker()
#         w.finished[int].connect(self.onFinished)
#         w.moveToThread(self.thread)
#         self.thread.started.connect(w.work)
#         self.thread.start()
#     @pyqtSlot(int)
#     def onFinished(self, i):
#         print("Base caught finished, {}".format(i))
class MyThread(QThread):
    monitor = None
    target = None
    signal = None
    def run(self):
        monitor = self.monitor
        @monitor.on("DANMU_MSG")
        async def recv(event):
            print('看开没开门卡哪款')
            # 发送者UID
            uid = event["data"]["info"][2][0]
            # 排除自己发送的弹幕
            # if uid == UID:
            #     return
            # 弹幕文本
            msg = event["data"]["info"][1]
            user_name = event["data"]["info"][2][1]
            # if msg == "你好":
            #     # 发送弹幕
            #     await sender.send_danmaku(Danmaku("你好！"))
            info = json.dumps(event)
            print(info)
            response = ''
            # if self.session_type == 'chatglm':
            #     if self.session == None:
            #         self.session = ChatglmSession()
            #     response = self.session.ask(msg, is_speak=True)
            # else:
            #     if self.langchain_session == None:
            #         self.langchain_session = LangchainSession()
            #     response, history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_base_name,
            #                                                               question=msg, history=[])
            # response = self.session.ask(msg,is_speak=True)
            print(response)
            info = event["data"]["info"]
            log.add(f'来自哔哩哔哩：[{user_name}(uid={uid}]:{msg}\n')
            # log.add(f'接收到弹幕：')
            # if '歌' in msg:
            #     self.audio_manager.test()
            #     return
            # try:
            info = {
                'nickname': user_name,
                'uid': uid,
                'message': msg
            }
            print('===============')
            # self.target.target.did_recieve_danmaku(info)
            self.signal.emit(info)
            # except:
            #     print('音频出现错误')
        sync(monitor.connect())

class bilibiliDanmaku(QObject):
    session: ChatglmSession = None
    audio_manager: AudioManager = None
    langchain_session:LangchainSession = None
    session_type:str = 'langchain'
    timer:threading.Timer = None
    target = None

    # def __init__(self) -> None:
    #     super.__init__()

    def start_server(self):
        knowledge_base_name = ''
        if self.session_type == 'chatglm':
            print('chatglm')
        else:
            # 选择知识库
            knowledge_lists = self.langchain_session.get_knowledge_lists()
            prompt = self.langchain_session.get_knowledge_prompt(knowledge_lists=knowledge_lists)
            print(prompt)
            selection = str(input('>> '))
            knowledge_base_name = knowledge_lists[int(selection)]

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
        # info = sync(sender.get_room_info())
        # info_json = json.dumps(info)
        # print(info_json)
        @monitor.on("DANMU_MSG")
        async def recv(event):
            # 发送者UID
            uid = event["data"]["info"][2][0]
            # 排除自己发送的弹幕
            # if uid == UID:
            #     return
            # 弹幕文本
            msg = event["data"]["info"][1]
            user_name = event["data"]["info"][2][1]
            # if msg == "你好":
            #     # 发送弹幕
            #     await sender.send_danmaku(Danmaku("你好！"))
            info = json.dumps(event)
            print(info)
            response = ''
            if self.session_type == 'chatglm':
                if self.session == None:
                    self.session = ChatglmSession()
                response = self.session.ask(msg, is_speak=True)
            else:
                if self.langchain_session == None:
                    self.langchain_session = LangchainSession()
                response,history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_base_name,question=msg,history=[])
            # response = self.session.ask(msg,is_speak=True)
            print(response)
            info = event["data"]["info"]
            log.add(f'来自哔哩哔哩：[{user_name}(uid={uid}]:{msg}\n   AI:{response}')
            # log.add(f'接收到弹幕：')
            if '歌' in msg:
                self.audio_manager.test()
                return
            try:
                speaker = Speaker()
                speaker.audio_manager = self.audio_manager
                speaker.speak(response)

                self.audio_manager.play(filename=speaker.output_path)
            except:
                print('音频出现错误')
        # 启动监听
        sync(monitor.connect())

    monitor = None
    thread = None
    def recive_danmaku_mainloop(self,info):
        print(info)
        print('收到子线程')
        self.target.did_recieve_danmaku(info)

    recive_event_signal:pyqtSignal = pyqtSignal(dict)

    def start_server_connect(self,roomid:str,credential:Credential,target):
        self.target = target
        # 自己直播间号
        ROOMID = roomid
        # 凭证 根据回复弹幕的账号填写
        # credential = Credential(
        #     sessdata="",
        #     bili_jct=""
        # )
        # 监听直播间弹幕
        monitor = LiveDanmaku(ROOMID, credential=credential)
        self.monitor = monitor
        # 用来发送弹幕
        sender = LiveRoom(ROOMID, credential=credential)
        # 自己的UID 可以手动填写也可以根据直播间号获取
        UID = sync(sender.get_room_info())["room_info"]["uid"]

        # info = sync(sender.get_room_info())
        # info_json = json.dumps(info)
        # print(info_json)
        # @monitor.on("DANMU_MSG")
        # async def recv(event):
            # # 发送者UID
            # uid = event["data"]["info"][2][0]
            # # 排除自己发送的弹幕
            # # if uid == UID:
            # #     return
            # # 弹幕文本
            # msg = event["data"]["info"][1]
            # user_name = event["data"]["info"][2][1]
            # # if msg == "你好":
            # #     # 发送弹幕
            # #     await sender.send_danmaku(Danmaku("你好！"))
            # info = json.dumps(event)
            # print(info)
            # response = ''
            # # if self.session_type == 'chatglm':
            # #     if self.session == None:
            # #         self.session = ChatglmSession()
            # #     response = self.session.ask(msg, is_speak=True)
            # # else:
            # #     if self.langchain_session == None:
            # #         self.langchain_session = LangchainSession()
            # #     response, history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_base_name,
            # #                                                               question=msg, history=[])
            # # response = self.session.ask(msg,is_speak=True)
            # print(response)
            # info = event["data"]["info"]
            # log.add(f'来自哔哩哔哩：[{user_name}(uid={uid}]:{msg}\n')
            # # log.add(f'接收到弹幕：')
            # # if '歌' in msg:
            # #     self.audio_manager.test()
            # #     return
            # try:
            #     info = {
            #         'nickname':user_name,
            #         'uid':uid,
            #         'message':msg
            #     }
            #     self.target.did_recieve_danmaku(info)
            # except:
            #     print('音频出现错误')

        # t = threading.Timer(1,monitor)
        # t.start()
        self.recive_event_signal.connect(self.recive_danmaku_mainloop)
        t = MyThread()
        t.monitor = monitor
        t.signal = self.recive_event_signal
        t.start()
        t.target = self
        self.thread = t




    def monitor_start(self,monitor):
        monitor = self.monitor
        @monitor.on("DANMU_MSG")
        async def recv(event):
            print('哈哈哈')

        monitor.connect()
        t = threading.Timer(1, monitor)
        t.start()

        # 启动监听
        # sync(monitor.connect())
        # thread = QThread()
        # thread.start()
        # thread.run()
        # monitor.connect()
        # thread.exit()


    def clear_credential_cache(self):
        if self.is_credential_exist():
            os.remove('Tmp/bilibili_credential.pickle')

    def restore_credential(self,credential:Credential = None):
        if credential == None:
            return
        print(credential)
        self.clear_credential_cache()

        with open('Tmp/bilibili_credential.pickle','wb') as f:
            pickle.dump(credential,f)

    def get_credential_cache(self):
        with open('Tmp/bilibili_credential.pickle','rb') as f:
            credential = pickle.load(f)
        return credential

    def is_credential_exist(self):
        is_exist = os.path.exists('Tmp/bilibili_credential.pickle')
        return is_exist


    qecode_data = None
    start = None
    credential = None
    is_destroy = False
    login_key = None
    def login_ui(self,qrcode_widget:QLabel,target) -> ():
        print('login')
        self.target = target
        is_needs_login = True
        if self.is_credential_exist() == True:
            is_needs_login = False
        credential = None


        if is_needs_login == True:
            print('显示二维码')
            # from PIL.ImageTk import PhotoImage
            # import tkinter
            # import tkinter.font

            # root = None
            # if root == None:
            #     root = tkinter.Tk()
            # root.title("扫码登录")

            # credential = login.login_with_qrcode()  # 使用窗口显示二维码登录
            # print('显示二维码')

            qrcode_data = login.update_qrcode_data()
            print(qrcode_data["url"])

            login_key = qrcode_data["qrcode_key"]
            self.login_key = login_key
            qrcode_image = login.make_qrcode(qrcode_data["url"])
            print(qrcode_image)
            # photo = PhotoImage(file=qrcode_image)
            # #
            img = QPixmap(qrcode_image).scaled(150,150,aspectRatioMode=Qt.KeepAspectRatio)
            qrcode_widget.setPixmap(img)
            qrcode_widget.setFixedSize(150,150)

            def update_events():
                login_key = self.login_key
                events = login.login_with_key(login_key)
                if "code" in events.keys() and events["code"] == 0:
                    if events["data"]["code"] == 86101:
                        # log.configure(text="请扫描二维码↑", fg="red", font=big_font)
                        print('请扫描二维码↑')
                        self.login_status_changed('请扫描二维码↓')
                    elif events["data"]["code"] == 86090:
                        # log.configure(text="点下确认啊！", fg="orange", font=big_font)
                        print('点下确认啊！')
                        self.login_status_changed('已扫描，请确认↓')
                    elif events["data"]["code"] == 86038:
                        # raise LoginError("二维码过期，请扫新二维码！")
                        print('二维码过期，请扫新二维码！')
                        self.login_status_changed('二维码过期，我也没办法...')
                    elif events["data"]["code"] == 0:
                        print('登录成功')
                        credential = login.parse_credential_url(events)
                        self.restore_credential(credential=credential)
                        self.login_success(credential=credential)
                        return 0
                    # if time.perf_counter() - start > 120:  # 刷新
                    #     qrcode_data = update_qrcode_data()
                    #     login_key = qrcode_data["qrcode_key"]
                        # qrcode_image = make_qrcode(qrcode_data["url"])
                        # photo = PhotoImage(file=qrcode_image)
                        # qrcode_label = tkinter.Label(root, image=photo, width=600, height=600)
                        # qrcode_label.pack()
                        # start = time.perf_counter()
                print('哈哈哈')
                timer = threading.Timer(1,update_events)
                timer.start()

            timer = threading.Timer(1,update_events)
            timer.start()

            # self.restore_credential(credential=credential)
            return None,None
        else:
            print('使用缓存登录')
            credential = self.get_credential_cache()


        credential, nickname = self.login_success(credential=credential)
        return credential,nickname

    def login_success(self,credential:Credential) -> ():
        try:
            credential.raise_for_no_bili_jct()  # 判断是否成功
            credential.raise_for_no_sessdata()  # 判断是否成功
        except:
            print("登陆失败。。。")
            # exit()
            # print("欢迎，", sync(user.get_self_info(credential))['name'], "!")
        nickname = sync(user.get_self_info(credential))['name']
        print(f'昵称:{nickname}')
        self.callback(nickname=nickname,credential=credential)
        return credential,nickname

    def login_status_changed(self,status:str):
        if self.target:
            try:
                self.target.login_status_changed(status)
            except:
                print('未定义target.login_finished({})')


    # 登录完成后回调
    def callback(self,nickname:str,credential:Credential):
        info = {
            'nickname':nickname,
            'credential':credential
        }
        if self.target:
            try:
                self.target.login_finished(info)
            except:
                print('未定义target.login_finished({})')
        self.target = None



    def start_server_ui(self):
        knowledge_base_name = ''
        if self.session_type == 'chatglm':
            print('chatglm')
        else:
            # 选择知识库
            knowledge_lists = self.langchain_session.get_knowledge_lists()
            prompt = self.langchain_session.get_knowledge_prompt(knowledge_lists=knowledge_lists)
            print(prompt)
            selection = str(input('>> '))
            knowledge_base_name = knowledge_lists[int(selection)]

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

        # info = sync(sender.get_room_info())
        # info_json = json.dumps(info)
        # print(info_json)
        @monitor.on("DANMU_MSG")
        async def recv(event):
            # 发送者UID
            uid = event["data"]["info"][2][0]
            # 排除自己发送的弹幕
            # if uid == UID:
            #     return
            # 弹幕文本
            msg = event["data"]["info"][1]
            user_name = event["data"]["info"][2][1]
            # if msg == "你好":
            #     # 发送弹幕
            #     await sender.send_danmaku(Danmaku("你好！"))
            info = json.dumps(event)
            print(info)
            response = ''
            if self.session_type == 'chatglm':
                if self.session == None:
                    self.session = ChatglmSession()
                response = self.session.ask(msg, is_speak=True)
            else:
                if self.langchain_session == None:
                    self.langchain_session = LangchainSession()
                response, history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_base_name,
                                                                          question=msg, history=[])
            # response = self.session.ask(msg,is_speak=True)
            print(response)
            info = event["data"]["info"]
            log.add(f'来自哔哩哔哩：[{user_name}(uid={uid}]:{msg}\n   AI:{response}')
            # log.add(f'接收到弹幕：')
            if '歌' in msg:
                self.audio_manager.test()
                return
            try:
                speaker = Speaker()
                speaker.audio_manager = self.audio_manager
                speaker.speak(response)

                self.audio_manager.play(filename=speaker.output_path)
            except:
                print('音频出现错误')

        # 启动监听
        sync(monitor.connect())

    def login(self):
        print("请登录：")
        # credential = login.login_with_qrcode_term() # 在终端扫描二维码登录
        is_needs_login = True
        if self.is_credential_exist() == True:
            is_needs_login == False
            selection = str(input('已有登录信息，是否重新登录？y/n\n>> '))
            if selection == 'y' or selection == 'Y':
                is_needs_login == True
            else:
                is_needs_login = False
        credential = None
        if is_needs_login == True:
            credential = login.login_with_qrcode()  # 使用窗口显示二维码登录
            self.restore_credential(credential=credential)
        else:
            print('使用缓存登录')
            credential = self.get_credential_cache()

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

    def destroy(self):
        try:
            if self.thread:
                self.thread.exit()
        except:
            print('')

