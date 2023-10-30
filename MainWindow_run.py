"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from PyQt5.QtWidgets import QDialog,QMainWindow
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
from MainWindow import Ui_MainWindow

# python -m PyQt5.uic.pyuic MainWindow.ui -o MainWindow.py
class MainWindowUI(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindowUI,self).__init__()
        self.setupUi(self)

        self.status = self.statusBar()  # 状态栏
        self.status.showMessage('', 0)  # 显示状态栏信息，默认为0(表示下一个操作前，一直显示状态栏；也可以设置显示时间，单位为毫秒)
        self.setWindowTitle('光线AI虚拟主播系统')  # 设置该窗口的名称

        self.pushButton.clicked.connect(self.click)
    # def setupUi(self, MainWindow):

    def click(self):
        print('哈哈哈哈哈哈哈哈')