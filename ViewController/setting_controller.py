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
from Utils.threading import EWThread
import time
from Session.request import *


class SettingController(BaseController):
    def setup_ui(self):
        super().setup_ui()
        self.window.page1_playtest_button.clicked.connect(self.play_test)
        self.window.pushButton_6.clicked.connect(self.connect_test)

        # 试音

    def play_test(self):
        player = Vtuber().audio_player.player
        if player.get_busy() is True:
            player.pause()
            self.window.page1_playtest_button.setText('试音')
            self.window.setting_status_label.setText('无')
        else:
            def completion_handler():
                self.window.page1_playtest_button.setText('试音')
                self.window.setting_status_label.setText('无')

            Vtuber().play_test(completion_handler=completion_handler)
            self.window.page1_playtest_button.setText('停止试音')
            self.window.setting_status_label.setText('当前正在试音...')

    def connect_test(self):
        # def process_handler(value_input = None):
        #     print(value)
        #     for i in range(0,15,1):
        #         time.sleep(1)
        #         print(i)
        #
        #     # time.sleep(5)
        #     print('process_handler')
        def request_finished(response):
            print('请求结束了')
            print(response)

        request = Request()
        request.post(url='http://www.baidu.com/a', headers={'key': 'value'}, query={'key_1': 'value1'},
                     parameters={'key11': 'value11'},
                     completion_handler=request_finished)

        # def completion_handler(value_input = None):
        #     print('completion_handler')
        #     print(value_input)
        #     self.window.pushButton_6.setText('成功')
        # thread = EWThread()
        # value = ['']
        # thread.start(process_handler=process_handler,completion_handler=completion_handler)
