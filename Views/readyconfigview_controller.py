"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
# python -m PyQt5.uic.pyuic Views/readyconfigview.ui -o Views/readyconfigview.py

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
from Views.readyconfigview import Ui_Form


class ReadyConfigView(Ui_Form,QDialog):

    def __init__(self):
        super(ReadyConfigView, self).__init__()
