"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from mainwindow import *
from PySide6.QtGui import QIcon


# pyside6-uic form.ui -o ui_form.py
# pyinstaller --noconsole --icon=Assets/Icon/icon.png -F app.py
# pyinstaller --noconsole --icon=Assets/Icon/icon.ico app.py
def application_start():
    """

    :param self:
    """
    application = QApplication(sys.argv)
    application.setWindowIcon(QIcon('Assets/Icon/icon.png'))  # 设置窗口的头标
    widget_1 = MainWindow()
    widget_1.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    application_start()
