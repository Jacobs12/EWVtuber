"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from ViewController.ewbase_controller import *


class SettingController(BaseController):

    def setup_ui(self):
        super().setup_ui()
        self.window.page1_playtest_button.clicked.connect(self.play_button_click)

    def play_button_click(self):
        if self.player().player.get_busy() is True:
            self.player().pause()
            self.window.page1_playtest_button.setText('播放')
            return
        if self.player().is_pause() is True:
            self.player().resume()
            self.window.page1_playtest_button.setText('暂停')
            return

        def play_finished():
            self.window.page1_playtest_button.setText('试音')

        self.window.page1_playtest_button.setText('暂停')
        self.player().test_completion_handler(play_finished)
