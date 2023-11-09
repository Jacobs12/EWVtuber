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


class Msg(object):
    user: str = ''
    message: str = ''


class CartoonController(BaseController):

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

    player: EWMediaPlayer = None
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
        print(self.reply_queue)

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
            self.window.cartoon_queue1_browser.setText(message)
            msg = self.reply_queue[1]
            message = f'>> {msg.user}:{msg.message}'
            self.window.cartoon_queue2_browser.setText(message)
        except:
            pass

    def reply(self):
        msg = self.pop_queue()
        print(msg.message)
        self.reload_queue()
        user_answer = f'>> {msg.user}:{msg.message}'

        reply = f'>> AI正在思考中...'
        message = f'{user_answer}\n{reply}'
        self.window.cartoon_replying_browser.setText(message)
        # t = threading.Thread(target=self.thinking(msg), name='thinking')
        # t.start()
        # t.join(15)
        asyncio.run(self.thinking(msg=msg))

    async def thinking(self, msg: Msg):
        user_answer = f'>> {msg.user}:{msg.message}'
        index = self.window.cartoon_knowledgelst_box.currentIndex()
        knowledge_selected = self.knowledge_lst[index]
        question = msg.message
        response, history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_selected,
                                                                  question=question, history=[])
        reply = f'>> AI:{response}'
        message = f'{user_answer}\n{reply}'
        self.window.cartoon_replying_browser.setText(message)

        # asyncio.run(speech.text_to_speech(text=response))
        # filepath = speech.text_to_speech(text=response)
        # vtuber.audio_player().play(filename=filepath)
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(speech.text_to_speech(text=response))
        # loop.close()
        await speech.text_to_speech(text=response)
        vtuber.audio_player().play(filename=speech.OUTPUT)

    def speak_button_click(self):
        text = self.window.cartoon_myquesition_field.toPlainText()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(speech.text_to_speech(text=text))
        loop.close()
        # speech.text_to_speech(text=text)
        vtuber.audio_player().play(filename=speech.OUTPUT)

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
        print(msg)
        self.push_queue(msg)
        self.reload_queue()
        self.window.cartoon_myquesition_field.setText('')

    def start_session(self):
        self.reply()

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

    def login_bilibili(self):
        print('1')
        self.bilibili_manager = bilibiliDanmaku()
        self.hide_qrcode(False)
        credential, nickname = self.bilibili_manager.login_ui(qrcode_widget=self.window.cartoon_qrcode_label)
        # self.window.shuziren_nickname_label.setText(str(nickname))

    def hide_qrcode(self, is_hidden: bool):
        self.window.cartoon_qrcode_label.setHidden(is_hidden)
        self.window.cartoon_qrcodecancel_button.setHidden(is_hidden)
        self.window.cartoon_login_button.setHidden(not is_hidden)
