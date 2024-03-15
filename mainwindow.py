# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from Controller.server_setting_controller import *
from Controller.server_tts_controller import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()
        self.setup_button()
        self.tts_button_click()

    def setup_ui(self):
        self.setup_controller()

    def setup_button(self):
        self.ui.tab_setting_button.clicked.connect(self.setting_button_click)
        self.ui.tab_tts_button.clicked.connect(self.tts_button_click)


    setting_controller:SettingController = None
    tts_controller:ServerTTSController = None
    def setup_controller(self):
        self.setting_controller = SettingController(window=self.ui)
        self.tts_controller = ServerTTSController(window=self.ui)



    def setting_button_click(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def tts_button_click(self):
        self.ui.stackedWidget.setCurrentIndex(2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
