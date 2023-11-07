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
from Platform.bilibili_livedanmaku import bilibiliDanmaku


class CartoonController(BaseController):
    def setup_ui(self):
        super().setup_ui()
        self.window.cartoon_videoplay_button.clicked.connect(self.play_video)
        self.hide_qrcode(True)
        self.window.cartoon_login_button.clicked.connect(self.login_bilibili)

    player: EWMediaPlayer = None

    def play_video(self):
        if self.player is None:
            self.player = EWMediaPlayer(widget=self.window.cartoon_video_widget)
        self.player.load_content_filepath('https://tb-video.bdstatic.com/tieba-smallvideo-transcode-crf/21_4c93be42b15bb2b0f0ff082827dc82c2_0.mp4?vt=0&pt=3&ver=&cr=2&cd=0&sid=&ft=2&tbau=2023-11-08_109fac1fd153bc5e5bbc070a8b4f241942ae24aa5c329db94e02d4a67eb3f012&ptid=8674226587')
        self.player.play()

    bilibili_manager = None

    def login_bilibili(self):
        print('1')
        self.bilibili_manager = bilibiliDanmaku()
        self.hide_qrcode(False)
        credential, nickname = self.bilibili_manager.login_ui(qrcode_widget=self.window.cartoon_qrcode_label)
        # self.window.shuziren_nickname_label.setText(str(nickname))

    def hide_qrcode(self,is_hidden:bool):
        self.window.cartoon_qrcode_label.setHidden(is_hidden)
        self.window.cartoon_qrcodecancel_button.setHidden(is_hidden)
        self.window.cartoon_login_button.setHidden(not is_hidden)


