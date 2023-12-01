"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import time

from ViewController.ewbase_controller import BaseController
from EWMedia.mediaplayer import EWMediaPlayer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Platform.bilibili_livedanmaku import bilibiliDanmaku
import requests
import json
import API.vtuber_api
from Utils.thread import *
from bilibili_api import Credential


class Msg(object):
    user: str = ''
    uid: str = ''
    message: str = ''
    status: int = 0  # 0-未回答 1-获取回答中 2-已回答
    thread: Thread = None
    knowledge: str = None
    response: str = None
    vid: str = None


class ShuzirenController(BaseController):
    player: EWMediaPlayer = None
    scripts_array = []

    def setup_ui(self):
        self.window.shuziren_video_button.clicked.connect(self.play_video)
        # img = QPixmap('Assets/Icon/icon.png').scaled(100,100,aspectRatioMode=Qt.KeepAspectRatio)
        # self.window.image_label.setPixmap(img)
        # self.window.image_label.setFixedSize(100,100)
        self.window.shuziren_login_button.clicked.connect(self.login_bilibili)
        self.window.shuziren_qrcode_label.setHidden(True)
        self.get_scripts_lists()
        self.window.shuziren_script_comboBox.currentIndexChanged.connect(self.script_title_changes)
        self.window.shuziren_script_listWidget.currentRowChanged.connect(self.script_content_changes)
        self.window.shuziren_script_button.clicked.connect(self.insert_script)
        self.window.shuziren_roomid_button.clicked.connect(self.connect_bilibili_server)
        self.hide_qrcode(True)

    t = None
    # 等待回复列表
    reply_queue: [] = []
    is_autonext = False

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
        self.window.shuziren_queue1_browser.setText('')
        self.window.shuziren_queue2_browser.setText('')
        try:
            msg = self.reply_queue[0]
            message = f'>> {msg.user}:{msg.message}'
            if msg.response is not None:
                message = f'>> {msg.user}:{msg.message}\n>> AI:{msg.response}'
            self.window.shuziren_queue1_browser.setText(message)
            msg = self.reply_queue[1]
            message = f'>> {msg.user}:{msg.message}'
            if msg.response is not None:
                message = f'>> {msg.user}:{msg.message}\n>> AI:{msg.response}'
            self.window.shuziren_queue2_browser.setText(message)
        except IndexError:
            print('IndexError')
        self.check_autoreply()

    player_thread = None

    is_replying = False

    def check_autoreply(self):
        if self.player_thread is not None or self.is_replying is True:
            return
        if self.is_autonext:
            self.reply()


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
        self.window.shuziren_replying_browser.setText(message)
        # t = threading.Thread(target=self.thinking(msg), name='thinking')
        # t.start()
        # t.join(15)
        # asyncio.run(self.thinking(msg=msg))
        self.msg = msg
        self.send_request(msg=msg)

    request_thread = None

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
        question = msg.message

        if msg.response is None:
            content = requests.get(f'http://172.23.0.191:10010/get_answer?question={question}')
            response_dic = json.loads(content.text)
            response = response_dic['a']
            msg.response = response
            msg.vid = response_dic['vid']
            self.insert_vid(msg.vid)
            self.request_thread.get_mainloop(message=response, func=self.ai_response)
        else:
            self.request_thread.get_mainloop(message=msg.response, func=self.ai_response)

    def ai_response(self, response: str):
        print(f'ai_response:{response}')
        msg = self.msg
        user_answer = f'>> {msg.user}:{msg.message}'
        reply = f'>> AI:{response}'
        message = f'{user_answer}\n{reply}'

        self.window.shuziren_replying_browser.setText(message)

    msg = None

    def play_video(self):
        if self.player is None:
            self.player = EWMediaPlayer(widget=self.window.video_widget)
        # self.player.load_content_filepath('Tmp/1.mp4')
        self.player.load_stream('rtmp://172.23.0.199:1935/live/stream')
        self.player.play()
        self.is_autonext = True

    # 话术
    def get_scripts_lists(self):
        try:
            url = API.vtuber_api.shuziren_script_lists()
            content = requests.get(url)
            response = content.text
            response_dic = json.loads(response)
            self.scripts_array = response_dic['lists']
            self.window.shuziren_script_comboBox.clear()
            for item in response_dic['lists']:
                self.window.shuziren_script_comboBox.addItem(item['title'])
            self.script_title_changes()
        except:
            pass

    def script_title_changes(self):
        try:
            index = self.window.shuziren_script_comboBox.currentIndex()
            script = self.scripts_array[index]
            scripts = script['content']
            lists = scripts['lists']
            self.window.shuziren_script_listWidget.clear()
            for video in lists:
                text = video['content']
                video_id = video['video_id']
                self.window.shuziren_script_listWidget.addItem(text)
            self.script_content_changes()
        except IndexError:
            pass

    def script_content_changes(self):
        try:
            index_row = self.window.shuziren_script_listWidget.currentIndex().row()
            index_section = self.window.shuziren_script_comboBox.currentIndex()
            script = self.scripts_array[index_section]
            scripts = script['content']
            lists = scripts['lists']
            item = lists[index_row]
            text = item['content']
            self.window.shuziren_script_textBrowser.setText(text)
        except IndexError:
            self.window.shuziren_script_textBrowser.setText('')

    # 插入话术队列
    def insert_script(self):
        index_row = self.window.shuziren_script_listWidget.currentIndex().row()
        index_section = self.window.shuziren_script_comboBox.currentIndex()
        script = self.scripts_array[index_section]
        scripts = script['content']
        lists = scripts['lists']
        item = lists[index_row]
        text = item['content']
        video_id = item['video_id']
        url = API.vtuber_api.shuziren_script_insert()
        response = requests.get(f'{url}?video_id={video_id}')
        print(response.text)

    #     登录
    bilibili_manager = None
    is_login = False
    bilibili_credential = None

    def login_bilibili(self):
        if self.is_login is True:
            self.is_login = False
            self.window.shuziren_nickname_label.setText('未登录')
            self.window.shuziren_login_button.setText('登录')
            self.bilibili_credential = None
            manager: bilibiliDanmaku = self.bilibili_manager
            manager.clear_credential_cache()
            manager.destroy()
            self.bilibili_manager = None
            return
        # print('1')
        self.bilibili_manager = bilibiliDanmaku()
        self.hide_qrcode(False)
        credential, nickname = self.bilibili_manager.login_ui(qrcode_widget=self.window.shuziren_qrcode_label,
                                                              target=self)

    def login_status_changed(self, status: str):
        self.window.shuziren_qrcodestatus_label.setText(status)
        self.window.shuziren_qrcodestatus_label.setStyleSheet("color: green")

    def login_finished(self, info):
        nickname = info['nickname']
        self.bilibili_credential = info['credential']
        self.window.shuziren_nickname_label.setText(nickname)
        self.hide_qrcode(True)
        self.window.shuziren_login_button.setText('退出登录')
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
        print(message)
        msg = Msg()
        msg.user = nickname
        msg.message = message
        self.window.shuziren_queue1_browser.setText(message)
        self.push_queue(msg)
        self.reload_queue()
        self.add_message(msg)

    message_thread_lst = []
    thread_tag: int = 100

    def add_message(self, msg: Msg):
        t = Thread()
        t.tag = self.thread_tag
        self.thread_tag += 1
        self.message_thread_lst.insert(0, t)
        msg.thread = t
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
        content = requests.get(f'http://172.23.0.191:10010/get_answer?question={question}')
        response_dic = json.loads(content.text)
        response = response_dic['a']
        msg.response = response
        msg.vid = response_dic['vid']
        self.insert_vid(msg.vid)
        t.get_mainloop(message=response, func=self.did_message_response)
        msg.thread = None
        self.message_thread_lst.remove(t)

    def did_message_response(self, response):
        self.reload_queue()

    def insert_vid(self, vid: str):
        try:
            requests.get(f'http://172.23.0.191:10010/insert_script?video_id={vid}')
        except:
            pass

    def hide_qrcode(self, is_hidden: bool):
        self.window.shuziren_qrcode_label.setHidden(is_hidden)
        self.window.shuziren_qrcodecancel_button.setHidden(is_hidden)
        self.window.shuziren_login_button.setHidden(not is_hidden)
        self.window.shuziren_qrcodestatus_label.setHidden(is_hidden)
