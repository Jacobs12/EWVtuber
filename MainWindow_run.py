"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
from MainWindow import Ui_MainWindow
from vtuber import Vtuber
from Views.readyconfigview_controller import ReadyConfigView
from Session.langchain_session import LangchainSession

from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

import vlc
import platform
from PyQt5 import QtWidgets, QtGui, QtCore
import os

# python -m PyQt5.uic.pyuic MainWindow.ui -o MainWindow.py
def config_button_click():
    app = QApplication(sys.argv)
    window = ReadyConfigView()
    window.setWindowTitle('')
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())


class MainWindowUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        self.setupUi(self)

        self.setup_window()
        self.setup_tabbar_button()
        self.setup_pages()

    # def setupUi(self, MainWindow):

    def setup_window(self):
        self.status = self.statusBar()  # 状态栏
        self.status.showMessage('', 0)  # 显示状态栏信息，默认为0(表示下一个操作前，一直显示状态栏；也可以设置显示时间，单位为毫秒)
        self.setWindowTitle('光线AI虚拟主播系统')  # 设置该窗口的名称

    # 设置菜单栏按钮
    def setup_tabbar_button(self):
        self.tab_bilibili_button.clicked.connect(self.bilibili_button_click)
        self.tab_llm_button.clicked.connect(self.llm_button_click)
        self.tab_shuziren_button.clicked.connect(self.shuziren_button_click)
        self.tab_knowledge_button.clicked.connect(self.knowledge_button_click)
        self.tab_knowledgemanage_button.clicked.connect(self.knowledge_manage_click)
        self.tab_ready_button.clicked.connect(self.setting_button_click)

    def setup_pages(self):
        self.stackedWidget.setCurrentIndex(0)
        self.setup_bilibili_homepage()
        self.setup_shuziren_homepage()
        self.setup_llm_homepage()
        self.setup_knowledge_homepage()
        self.setup_knowledge_manage()
        self.setup_setting_homepage()

    # 设置哔哩哔哩直播页面
    def setup_bilibili_homepage(self):
        print('')

    #     设置llm聊天界面
    def setup_llm_homepage(self):
        print('')
        self.llm_sender_button.clicked.connect(self.llm_send_click)

    # 设置数字人直播界面
    instance: vlc = None
    player = None
    videoframe = None
    palette = None

    def setup_shuziren_homepage(self):
        print('数字人')
        self.shuziren_video_button.clicked.connect(self.play_video)
        # self.player = QMediaPlayer()
        # creating a basic vlc instance
        # In this widget, the video will be drawn
        if platform.system() == "Darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.player = self.instance.media_player_new()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

    # 设置知识库问答界面
    def setup_knowledge_homepage(self):
        print('')

    #     设置知识库管理界面
    def setup_knowledge_manage(self):
        print('')

    # 设置设置界面
    def setup_setting_homepage(self):
        print('')
        self.page1_playtest_button.clicked.connect(self.play_test)

    # 试音
    def play_test(self):
        Vtuber().play_test()
        self.page1_playtest_button.setText('暂停')

    # 菜单按钮点击
    def bilibili_button_click(self):
        self.stackedWidget.setCurrentIndex(0)

    def llm_button_click(self):
        self.stackedWidget.setCurrentIndex(1)

    def shuziren_button_click(self):
        self.stackedWidget.setCurrentIndex(2)

    def knowledge_button_click(self):
        self.stackedWidget.setCurrentIndex(3)

    def knowledge_manage_click(self):
        self.stackedWidget.setCurrentIndex(4)

    def setting_button_click(self):
        self.stackedWidget.setCurrentIndex(5)

    def play_video(self):
        # dialog_txt = "选择本地视频"
        # filename = QtWidgets.QFileDialog.getOpenFileName(self, dialog_txt, os.path.expanduser('~'))
        # if not filename:
        #     return
        # print(filename)
        # # getOpenFileName returns a tuple, so use only the actual file name
        # media = self.instance.media_new(filename[0])
        media = self.instance.media_new('rtmp://172.23.0.199:1935/live/stream')
        # Put the media in the media player
        self.player.set_media(media)

        # Parse the metadata of the file
        media.parse()

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux":  # for Linux using the X Server
            self.player.set_xwindow(int(self.video_widget.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.player.set_hwnd(int(self.video_widget.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.player.set_nsobject(int(self.video_widget.winId()))
        self.player.play()

    #         LLM聊天
    llm_history: list = []

    # LLM聊天模式回复label
    def llm_send_click(self):
        question = self.llm_input_field.toPlainText()
        if question == '' or question is None:
            self.llm_response_field.setText('您没有输入任何内容')
        session = LangchainSession()
        self.llm_input_field.setText('')
        response, history = session.chat_normal(question=question, history=self.llm_history)
        print(question)
        value = f'>> 用户：{question}\nAI：{response}\n\n{self.llm_response_field.toPlainText()}'
        self.llm_response_field.setText(value)
