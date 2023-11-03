"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from ViewController.ewbase_controller import BaseController
from vtuber import Vtuber


class SettingController(BaseController):
    def setup_ui(self):
        super().setup_ui()
        self.window.page1_playtest_button.clicked.connect(self.play_test)

        # 试音

    def play_test(self):
        player = Vtuber().audio_player.player
        if player.get_busy() is True:
            player.pause()
            self.window.page1_playtest_button.setText('试音')
            self.window.setting_status_label.setText('无')
        else:
            Vtuber().play_test()
            self.window.page1_playtest_button.setText('停止试音')
            self.window.setting_status_label.setText('当前正在试音...')
