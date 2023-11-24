"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import threading
import time
import asyncio

import Utils.utils
from ViewController.ewbase_controller import BaseController
from EWMedia.mediaplayer import EWMediaPlayer
from Platform.bilibili_livedanmaku import bilibiliDanmaku
from EWMedia.camera_capture import CameraCapture
from Session.langchain_session import LangchainSession
import vtuber
import EWSpeech.edge_speech as speech
from Audio.player import AudioPlayer
from EWSpeech.edge_speech import EdgeSpeech
from bilibili_api import Credential

from Utils.thread import *


class Msg(object):
    user: str = ''
    uid: str = ''
    message: str = ''
    status: int = 0  # 0-未回答 1-获取回答中 2-已回答
    thread: Thread = None
    knowledge: str = None
    response: str = None


class CartoonController(BaseController):
    is_login: bool = False
    is_autonext = False

    def init(self):
        self.init_session()

    def setup_ui(self):
        super().setup_ui()
        self.window.cartoon_videoplay_button.clicked.connect(self.play_video)
        self.hide_qrcode(True)
        self.window.cartoon_login_button.clicked.connect(self.login_bilibili)
        self.window.cartoon_sendquesion_button.clicked.connect(self.send_my_question)
        self.window.cartoon_sessionstart_button.clicked.connect(self.start_session)
        self.window.cartoon_speak_button.clicked.connect(self.speak_button_click)
        self.window.cartoon_roomconnect_button.clicked.connect(self.connect_bilibili_server)

    camera: CameraCapture = None

    """
    知识库问答
    """
    # 本地知识库会话类
    langchain_session: LangchainSession = None
    # 本地知识库列表
    knowledge_lst: [] = None
    # 等待回复列表
    reply_queue: [] = []

    # 初始化对话

    def push_queue(self, message: Msg):
        self.reply_queue.insert(0, message)
        if len(self.reply_queue) > 3:
            lst = self.reply_queue
            self.reply_queue = [lst[0], lst[1], lst[2]]
        # print(self.reply_queue)

    def pop_queue(self):
        if len(self.reply_queue) == 0:
            return None
        msg = self.reply_queue[0]
        self.reply_queue.remove(msg)
        return msg

    def reload_queue(self):
        self.window.cartoon_queue1_browser.setText('')
        self.window.cartoon_queue2_browser.setText('')
        try:
            msg = self.reply_queue[0]
            message = f'>> {msg.user}:{msg.message}'
            if msg.response is not None:
                message = f'>> {msg.user}:{msg.message}\n>> AI:{msg.response}'
            self.window.cartoon_queue1_browser.setText(message)
            msg = self.reply_queue[1]
            message = f'>> {msg.user}:{msg.message}'
            if msg.response is not None:
                message = f'>> {msg.user}:{msg.message}\n>> AI:{msg.response}'
            self.window.cartoon_queue2_browser.setText(message)
        except IndexError:
            pass
        self.check_autoreply()

    msg = None

    def check_autoreply(self):
        if self.player_thread is not None or self.is_replying is True:
            return
        if self.is_autonext:
            self.reply()

    is_replying = False

    def reply(self):
        msg = self.pop_queue()
        if msg is None:
            return
        else:
            self.is_replying = True
        # print(msg.message)
        self.reload_queue()
        user_answer = f'>> {msg.user}:{msg.message}'

        reply = f'>> AI正在思考中...'
        message = f'{user_answer}\n{reply}'
        self.window.cartoon_replying_browser.setText(message)
        # t = threading.Thread(target=self.thinking(msg), name='thinking')
        # t.start()
        # t.join(15)
        # asyncio.run(self.thinking(msg=msg))
        self.msg = msg
        self.send_request(msg=msg)

    speaker: EdgeSpeech = None
    player: AudioPlayer = None
    request_thread: Thread() = None

    def send_request(self, msg: Msg):
        if self.request_thread is not None:
            print('请等待问答完成')
            return
        t = Thread()
        self.request_thread = t
        t.start(func=self.thinking)

    def thinking(self):
        msg = self.msg
        user_answer = f'>> {msg.user}:{msg.message}'
        index = self.window.cartoon_knowledgelst_box.currentIndex()
        knowledge_selected = self.knowledge_lst[index]
        question = msg.message
        response = None
        history = []
        if msg.response is None:
            response, history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_selected,
                                                                      question=question, history=[])
            self.request_thread.get_mainloop(message=response, func=self.ai_response)
        else:
            self.request_thread.get_mainloop(message=msg.response, func=self.ai_response)

    def ai_response(self, response: str):
        print(f'ai_response:{response}')
        msg = self.msg
        user_answer = f'>> {msg.user}:{msg.message}'
        reply = f'>> AI:{response}'
        message = f'{user_answer}\n{reply}'

        self.window.cartoon_replying_browser.setText(message)

        # asyncio.run(speech.text_to_speech(text=response))
        # filepath = speech.text_to_speech(text=response)
        # vtuber.audio_player().play(filename=filepath)
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(speech.text_to_speech(text=response))
        # loop.close()
        # player = vtuber.audio_player().player
        # try:
        #     player.unload()
        # finally:
        #     pass
        # await speech.text_to_speech(text=response)
        # vtuber.audio_player().player.play(filename=speech.OUTPUT)
        # if self.player is None:
        #     self.player = vtuber.audio_player()
        # else:
        #     self.player.player.unload()
        # if self.speaker is None:
        #     self.speaker = EdgeSpeech()
        text = f'有位网友问:{msg.message},  {response}'
        # # await self.speaker.text_to_speech(text=text)
        # # # speech.text_to_speech(text=text)
        # # self.speaker = speech.EdgeSpeech()
        # # self.player.play(filename=speech.OUTPUT)
        # self.speak_response(response=text)
        if self.player is None:
            self.player = vtuber.audio_player()
        else:
            self.player.player.unload()
        if self.speaker is None:
            self.speaker = EdgeSpeech()
        self.speak_response(text)

    text: str = ''

    def speak_button_click(self):
        if self.player is None:
            self.player = vtuber.audio_player()
        else:
            self.player.player.unload()
        if self.speaker is None:
            self.speaker = EdgeSpeech()
        text = self.window.cartoon_myquesition_field.toPlainText()
        self.speak_response(text)

    audio_thread = None

    def speak_response(self, response: str):
        if self.audio_thread is not None:
            print('请等待当前任务完成')
            return
        self.text = response
        t = Thread()
        self.audio_thread = t
        t.start(func=self.generate_audio)

    def generate_audio(self):
        text = self.text
        asyncio.run(self.speaker.text_to_speech(text=text))
        self.audio_thread.get_mainloop(message='success', func=self.play_audio)

    player_timer = None

    player_thread = None

    def play_audio(self, message):
        print(message)
        self.player.play(filename=speech.OUTPUT)
        self.audio_thread.destroy()
        self.audio_thread = None
        if self.request_thread:
            self.request_thread.destroy()
            self.request_thread = None
        if self.player_thread is None:
            self.player_thread = Thread()
            self.player_thread.start(func=self.observe_player)

    def observe_player(self):
        while True:
            print('监听')
            time.sleep(1.0)
            if self.player.player.get_busy() is True:
                print('当前正在播放')
                continue

            print('播放结束了')
            self.player_thread.get_mainloop(message='', func=self.player_did_finished)
            break

    def player_did_finished(self, value):
        self.player_thread.destroy()
        self.player_thread = None
        self.is_replying = False
        self.check_autoreply()

    def init_session(self):
        # 初始化知识库列表
        if self.langchain_session is None:
            self.langchain_session = LangchainSession()
        knowledge_lst = self.langchain_session.get_knowledge_lists()
        self.window.cartoon_knowledgelst_box.clear()
        self.window.cartoon_knowledgelst_box.addItems(knowledge_lst)
        self.knowledge_lst = knowledge_lst

    def send_my_question(self, question: str):
        message = self.window.cartoon_myquesition_field.toPlainText()
        msg = Msg()
        msg.user = "主播"
        msg.message = message
        # print(msg)
        self.push_queue(msg)
        self.reload_queue()
        self.window.cartoon_myquesition_field.setText('')
        self.add_message(msg)

    def start_session(self):
        self.is_autonext = not self.is_autonext
        if self.is_autonext is True:
            self.reply()
            self.window.cartoon_sessionstart_button.setText('停止')
        else:
            self.player.pause()
            self.window.cartoon_sessionstart_button.setText('开始')

    """
    监控画面模块
    """

    # 播放监控画面
    def play_video(self):
        # if self.player is None:
        #     self.player = EWMediaPlayer(widget=self.window.cartoon_video_widget)
        # self.player.load_content_filepath('https://tb-video.bdstatic.com/tieba-smallvideo-transcode-crf/21_4c93be42b15bb2b0f0ff082827dc82c2_0.mp4?vt=0&pt=3&ver=&cr=2&cd=0&sid=&ft=2&tbau=2023-11-08_109fac1fd153bc5e5bbc070a8b4f241942ae24aa5c329db94e02d4a67eb3f012&ptid=8674226587')
        # self.player.play()
        # self.player.load_camera()
        # self.player.play()
        # print(Utils.utils.get_camera_mrl())
        if self.camera is None:
            index = self.window.cartoon_channel_box.currentIndex()
            self.camera = CameraCapture(video_label=self.window.cartoon_video_label, channel=index)
        self.camera.open_camera()

    bilibili_manager = None
    bilibili_credential = None

    """
    哔哩哔哩登录
    """

    def login_bilibili(self):
        if self.is_login is True:
            self.is_login = False
            self.window.cartoon_nickname_label.setText('未登录')
            self.window.cartoon_login_button.setText('登录')
            self.bilibili_credential = None
            manager: bilibiliDanmaku = self.bilibili_manager
            manager.clear_credential_cache()
            manager.destroy()
            self.bilibili_manager = None
            return
        # print('1')
        self.bilibili_manager = bilibiliDanmaku()
        self.hide_qrcode(False)
        credential, nickname = self.bilibili_manager.login_ui(qrcode_widget=self.window.cartoon_qrcode_label,
                                                              target=self)
        # self.window.shuziren_nickname_label.setText(str(nickname))

    def login_status_changed(self, status: str):
        self.window.cartoon_qrcodestatus_label.setText(status)
        self.window.cartoon_qrcodestatus_label.setStyleSheet("color: green")

    def login_finished(self, info):
        nickname = info['nickname']
        self.bilibili_credential = info['credential']
        self.window.cartoon_nickname_label.setText(nickname)
        self.hide_qrcode(True)
        self.window.cartoon_login_button.setText('退出登录')
        self.is_login = True

    def connect_bilibili_server(self):
        if self.bilibili_credential is None:
            print('未登录')
            return
        roomid = self.window.cartoon_roomid_lineedit.text()
        print(roomid)
        manager: bilibiliDanmaku = self.bilibili_manager
        manager.start_server_connect(roomid=roomid, credential=self.bilibili_credential, target=self)

    def did_recieve_danmaku(self, danmaku):
        nickname = danmaku['nickname']
        uid = danmaku['uid']
        message = danmaku['message']
        msg = Msg()
        msg.user = nickname
        msg.message = message
        self.push_queue(msg)
        self.reload_queue()
        self.add_message(msg)
        # self.window.cartoon_queue1_browser.setText(danmaku)

    message_thread_lst = []
    thread_tag: int = 100

    def add_message(self, msg: Msg):
        print('')
        t = Thread()
        t.tag = self.thread_tag
        self.thread_tag += 1
        self.message_thread_lst.insert(0, t)
        msg.thread = t
        index = self.window.cartoon_knowledgelst_box.currentIndex()
        knowledge_selected = self.knowledge_lst[index]
        msg.knowledge = knowledge_selected
        t.start(func=self.run_message_request)

    def run_message_request(self):
        t = self.message_thread_lst[0]
        msg = None
        for obj in self.reply_queue:
            if obj.thread is None:
                continue
            if obj.thread.tag == t.tag:
                msg = obj
        if msg is None:
            return
        question = msg.message
        knowledge_selected = msg.knowledge
        response, history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_selected,
                                                                  question=question, history=[])
        msg.response = response
        t.get_mainloop(message=response, func=self.did_message_response)
        msg.thread = None
        self.message_thread_lst.remove(t)

    def did_message_response(self, response):
        self.reload_queue()

    def hide_qrcode(self, is_hidden: bool):
        self.window.cartoon_qrcode_label.setHidden(is_hidden)
        self.window.cartoon_qrcodecancel_button.setHidden(is_hidden)
        self.window.cartoon_login_button.setHidden(not is_hidden)
        self.window.cartoon_qrcodestatus_label.setHidden(is_hidden)
