"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from ViewController.ewbase_controller import BaseController
from EWMedia.mediaplayer import EWMediaPlayer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Platform.bilibili_livedanmaku import bilibiliDanmaku
import requests
import json
import API.vtuber_api


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

    def play_video(self):
        if self.player is None:
            self.player = EWMediaPlayer(widget=self.window.video_widget)
        # self.player.load_content_filepath('Tmp/1.mp4')
        self.player.load_stream('rtmp://172.23.0.199:1935/live/stream')
        self.player.play()

    bilibili_manager = None
    def login_bilibili(self):
        print('1')
        self.bilibili_manager = bilibiliDanmaku()
        self.window.shuziren_qrcode_label.setHidden(False)
        credential,nickname = self.bilibili_manager.login_ui(qrcode_widget=self.window.shuziren_qrcode_label)
        # self.window.shuziren_nickname_label.setText(str(nickname))

    def get_scripts_lists(self):
        url = API.vtuber_api.shuziren_script_lists()
        content = requests.get(url)
        response = content.text
        response_dic = json.loads(response)
        self.scripts_array = response_dic['lists']
        self.window.shuziren_script_comboBox.clear()
        for item in response_dic['lists']:
            self.window.shuziren_script_comboBox.addItem(item['title'])
        self.script_title_changes()

    def script_title_changes(self):
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


