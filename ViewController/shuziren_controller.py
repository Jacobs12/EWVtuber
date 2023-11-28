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

    def play_video(self):
        if self.player is None:
            self.player = EWMediaPlayer(widget=self.window.video_widget)
        # self.player.load_content_filepath('Tmp/1.mp4')
        self.player.load_stream('rtmp://172.23.0.199:1935/live/stream')
        self.player.play()


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
        # msg = Msg()
        # msg.user = nickname
        # msg.message = message
        # self.push_queue(msg)
        # self.reload_queue()
        # self.add_message(msg)
        # self.window.cartoon_queue1_browser.setText(danmaku)

    # message_thread_lst = []
    # thread_tag: int = 100

    # def add_message(self, msg: Msg):
    #     print('')
    #     t = Thread()
    #     t.tag = self.thread_tag
    #     self.thread_tag += 1
    #     self.message_thread_lst.insert(0, t)
    #     msg.thread = t
    #     index = self.window.cartoon_knowledgelst_box.currentIndex()
    #     knowledge_selected = self.knowledge_lst[index]
    #     msg.knowledge = knowledge_selected
    #     t.start(func=self.run_message_request)
    #
    # def run_message_request(self):
    #     t = self.message_thread_lst[0]
    #     msg = None
    #     for obj in self.reply_queue:
    #         if obj.thread is None:
    #             continue
    #         if obj.thread.tag == t.tag:
    #             msg = obj
    #     if msg is None:
    #         return
    #     question = msg.message
    #     knowledge_selected = msg.knowledge
    #     response, history = self.langchain_session.chat_knowledge(knowledge_base_name=knowledge_selected,
    #                                                               question=question, history=[])
    #     msg.response = response
    #     t.get_mainloop(message=response, func=self.did_message_response)
    #     msg.thread = None
    #     self.message_thread_lst.remove(t)
    #
    # def did_message_response(self, response):
    #     self.reload_queue()

    def hide_qrcode(self, is_hidden: bool):
        self.window.shuziren_qrcode_label.setHidden(is_hidden)
        self.window.shuziren_qrcodecancel_button.setHidden(is_hidden)
        self.window.shuziren_login_button.setHidden(not is_hidden)
        self.window.shuziren_qrcodestatus_label.setHidden(is_hidden)
