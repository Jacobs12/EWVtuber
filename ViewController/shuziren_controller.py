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


class ShuzirenController(BaseController):
    player: EWMediaPlayer = None

    def setup_ui(self):
        self.window.shuziren_video_button.clicked.connect(self.play_video)
        # img = QPixmap('Assets/Icon/icon.png').scaled(100,100,aspectRatioMode=Qt.KeepAspectRatio)
        # self.window.image_label.setPixmap(img)
        # self.window.image_label.setFixedSize(100,100)
        self.window.shuziren_login_button.clicked.connect(self.login_bilibili)
        self.window.shuziren_qrcode_label.setHidden(True)

    def play_video(self):
        if self.player is None:
            self.player = EWMediaPlayer(widget=self.window.video_widget)
        self.player.load_content_filepath('Tmp/1.mp4')
        self.player.play()

    bilibili_manager = None
    def login_bilibili(self):
        print('1')
        self.bilibili_manager = bilibiliDanmaku()
        self.window.shuziren_qrcode_label.setHidden(False)
        credential,nickname = self.bilibili_manager.login_ui(qrcode_widget=self.window.shuziren_qrcode_label)
        # self.window.shuziren_nickname_label.setText(str(nickname))
