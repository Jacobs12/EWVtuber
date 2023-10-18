'''
Author: wolffy
Date: 2023-10-18 14:02:35
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-18 14:38:45
FilePath: /EWVtuber/Platform/bilibili_livedanmaku.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved. 
'''
from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom
from Session.chatglm_session import ChatglmSession
from EWSpeech.speech import Speaker

class bilibiliDanmaku(object):

    session : ChatglmSession = None
    def __init__(self) -> None:
        pass

    def startServer(self):
        # 自己直播间号
        ROOMID = 30923980
        # 凭证 根据回复弹幕的账号填写
        credential = Credential(
            sessdata="",
            bili_jct=""
        )
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
            if uid == UID:
                return
            # 弹幕文本
            msg = event["data"]["info"][1]
            # if msg == "你好":
            #     # 发送弹幕
            #     await sender.send_danmaku(Danmaku("你好！"))

            response = self.session.ask(msg)
            print(response)
            speaker = Speaker(response)
            speaker.speak(response)

        # 启动监听
        sync(monitor.connect())