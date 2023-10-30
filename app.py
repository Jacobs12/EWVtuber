"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import sys

from MainWindow import Ui_MainWindow
from vtuber import Vtuber
import os
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from MainWindow_run import MainWindowUI

# import sys
# from PyQt5.QtWidgets import QWidget, QApplication

# python=3.9.18

# -i https://pypi.tuna.tsinghua.edu.cn

# https://mirrors.aliyun.com/pypi/simple/

def main_window() -> Ui_MainWindow:
    print('')
    app = QApplication(sys.argv)  # 是PyQt的整个后台管理的命脉
    app.setWindowIcon(QIcon('Assets/Icon/icon.png'))  # 设置窗口的头标
    # form = Ui_MainWindow()  # 调用MainWindow类，并进行显示
    # # form.show()
    # sys.exit(app.exec_())  # 运行主循环，必须调用此函数才可以开始事件处理
    # app = QtWidgets.QApplication(sys.argv)
    #
    # window = uic.loadUi("MainWindow.ui")
    #
    window = MainWindowUI()
    window.show()
    #
    # ui = Ui_MainWindow()
    # ui.setupUi(window)
    app.exec()
    return window


if __name__ == '__main__':
    print('欢迎使用光线AI虚拟主播系统')
    app = Vtuber()
    # app.start_command_line()
    select = str(input('请输入界面模式：\n  1.命令行模式\n  2.可视化界面\n>> '))
    if select == '1':
        app.start_command_line()
    elif select == '2':
        # print('可视化界面正在开发中')
        window = main_window()
        app.window = window
        app.setup_ui()
    else:
        print('无效的参数')
