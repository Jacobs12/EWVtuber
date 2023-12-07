"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from ViewController.ewbase_controller import BaseController
from Utils.thread import *


class Msg(object):
    type: int = 0  # 0 - 弹幕，1 - 讲故事
    user: str = ''
    uid: str = ''
    message: str = ''
    status: int = 0  # 0-未回答 1-获取回答中 2-已回答
    thread: Thread = None
    knowledge: str = None
    response: str = None

    # session_selected 0-本地知识库,1-llm问答
    def get_ai_response(self,session_selected:int = 1):
        if session_selected == 0:
            # 本地知识库问答
            print('本地知识库问答')
        elif session_selected == 1:
            print('llm问答')
        

class CartoonViewController(BaseController):
    def setup_ui(self):
        super().setup_ui()
        self.window.cartoon_videoplay_button.clicked.connect(self.play_video)
        self.hide_qrcode(True)
        self.window.cartoon_login_button.clicked.connect(self.login_bilibili)
        self.window.cartoon_sendquesion_button.clicked.connect(self.send_my_question)
        self.window.cartoon_sessionstart_button.clicked.connect(self.start_session)
        self.window.cartoon_speak_button.clicked.connect(self.speak_button_click)
        self.window.cartoon_roomconnect_button.clicked.connect(self.connect_bilibili_server)

    def hide_qrcode(self, is_hidden: bool):
        self.window.cartoon_qrcode_label.setHidden(is_hidden)
        self.window.cartoon_qrcodecancel_button.setHidden(is_hidden)
        self.window.cartoon_login_button.setHidden(not is_hidden)
        self.window.cartoon_qrcodestatus_label.setHidden(is_hidden)

    # 登录
    def login_bilibili(self):
        print('')

    def connect_bilibili_server(self):
        print('')

    def play_video(self):
        print('')



    def send_my_question(self):
        print('')

    def start_session(self):
        print('')

    def speak_button_click(self):
        print('')


