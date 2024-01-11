"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
# import sys
#
# import Utils.utils
# from MainWindow import Ui_MainWindow
# from vtuber import Vtuber
# import os
# from PyQt5.QtWidgets import QDialog
# from PyQt5 import QtWidgets
# from PyQt5 import uic
import sys
import time

import Tools.audio
from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from MainWindow_run import MainWindowUI

# import sys
# from PyQt5.QtWidgets import QWidget, QApplication
from Tools.audio import *


# python=3.9.18

# -i https://pypi.tuna.tsinghua.edu.cn

# https://mirrors.aliyun.com/pypi/simple/

def main_window() -> Ui_MainWindow:
    application = QApplication(sys.argv)  # 是PyQt的整个后台管理的命脉
    application.setWindowIcon(QIcon('Assets/Icon/icon.png'))  # 设置窗口的头标
    window_ui = MainWindowUI()
    window_ui.show()
    application.exec()
    return window_ui


if __name__ == '__main__':
    window = main_window()
