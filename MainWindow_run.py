"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from MainWindow import Ui_MainWindow
from vtuber import Vtuber
from PyQt5.QtWidgets import *

from ViewController.cartoon_controller import CartoonController
from ViewController.shuziren_controller import ShuzirenController
from ViewController.llm_controller import LLMController
from ViewController.setting_controller import SettingController


# python -m PyQt5.uic.pyuic MainWindow.ui -o MainWindow.py

class MainWindowUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        self.setupUi(self)

        self.setup_window()
        self.setup_tabbar_button()
        self.setup_pages()

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

    # 设置应用界面
    def setup_pages(self):
        # 默认显示第一页界面
        self.stackedWidget.setCurrentIndex(0)
        self.setup_bilibili_homepage()
        self.setup_shuziren_homepage()
        self.setup_llm_homepage()
        self.setup_knowledge_homepage()
        self.setup_knowledge_manage()
        self.setup_setting_homepage()

# """
# ===========================================================================
#                             设置应用界面
# ===========================================================================
# """

    # 设置哔哩哔哩直播页面
    bilibili_controller: CartoonController = None

    def setup_bilibili_homepage(self):
        self.bilibili_controller = CartoonController(window=self)

    #     设置llm聊天界面
    llm_controller: LLMController = None

    def setup_llm_homepage(self):
        print('')
        self.llm_controller = LLMController(window=self)

    # 设置数字人直播界面
    shuziren_controller: ShuzirenController = None

    def setup_shuziren_homepage(self):
        self.shuziren_controller = ShuzirenController(window=self)

    # 设置知识库问答界面
    def setup_knowledge_homepage(self):
        print('')

    #     设置知识库管理界面
    def setup_knowledge_manage(self):
        print('')

    # 设置设置界面

    setting_controller: SettingController = None

    def setup_setting_homepage(self):
        print('')
        self.setting_controller = SettingController(window=self)

# """
# ===========================================================================
#                           菜单按钮点击
# ===========================================================================
# """
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
