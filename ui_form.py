# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStackedWidget,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 10, 100, 32))
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(130, 0, 821, 601))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 40, 81, 16))
        self.setting_projectfolder_button = QPushButton(self.page)
        self.setting_projectfolder_button.setObjectName(u"setting_projectfolder_button")
        self.setting_projectfolder_button.setGeometry(QRect(110, 33, 100, 32))
        self.setting_projectfolder_label = QLabel(self.page)
        self.setting_projectfolder_label.setObjectName(u"setting_projectfolder_label")
        self.setting_projectfolder_label.setGeometry(QRect(220, 40, 421, 16))
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(35, 130, 58, 16))
        self.setting_speaker_combo = QComboBox(self.page)
        self.setting_speaker_combo.addItem("")
        self.setting_speaker_combo.setObjectName(u"setting_speaker_combo")
        self.setting_speaker_combo.setGeometry(QRect(106, 120, 221, 32))
        self.setting_speaker_button = QPushButton(self.page)
        self.setting_speaker_button.setObjectName(u"setting_speaker_button")
        self.setting_speaker_button.setGeometry(QRect(350, 120, 100, 32))
        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 95, 101, 16))
        self.setting_standby_button = QPushButton(self.page)
        self.setting_standby_button.setObjectName(u"setting_standby_button")
        self.setting_standby_button.setGeometry(QRect(130, 90, 100, 32))
        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(290, 95, 101, 16))
        self.setting_script_button = QPushButton(self.page)
        self.setting_script_button.setObjectName(u"setting_script_button")
        self.setting_script_button.setGeometry(QRect(400, 90, 100, 32))
        self.setting_qa_button = QPushButton(self.page)
        self.setting_qa_button.setObjectName(u"setting_qa_button")
        self.setting_qa_button.setGeometry(QRect(630, 90, 100, 32))
        self.label_5 = QLabel(self.page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(560, 95, 101, 16))
        self.label_6 = QLabel(self.page)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(190, 65, 141, 21))
        self.setting_resource_button = QPushButton(self.page)
        self.setting_resource_button.setObjectName(u"setting_resource_button")
        self.setting_resource_button.setGeometry(QRect(340, 60, 100, 32))
        self.setting_prebuild_button = QPushButton(self.page)
        self.setting_prebuild_button.setObjectName(u"setting_prebuild_button")
        self.setting_prebuild_button.setGeometry(QRect(30, 60, 100, 32))
        self.setting_standby_label = QLabel(self.page)
        self.setting_standby_label.setObjectName(u"setting_standby_label")
        self.setting_standby_label.setGeometry(QRect(240, 95, 41, 16))
        self.setting_script_label = QLabel(self.page)
        self.setting_script_label.setObjectName(u"setting_script_label")
        self.setting_script_label.setGeometry(QRect(510, 95, 41, 16))
        self.setting_qa_label = QLabel(self.page)
        self.setting_qa_label.setObjectName(u"setting_qa_label")
        self.setting_qa_label.setGeometry(QRect(740, 95, 41, 16))
        self.setting_resource_label = QLabel(self.page)
        self.setting_resource_label.setObjectName(u"setting_resource_label")
        self.setting_resource_label.setGeometry(QRect(450, 65, 41, 16))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1080, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u9879\u76ee\u6587\u4ef6\u5939\uff1a", None))
        self.setting_projectfolder_button.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9", None))
        self.setting_projectfolder_label.setText(QCoreApplication.translate("MainWindow", u"\u672a\u9009\u62e9", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u8bed\u97f3\uff1a", None))
        self.setting_speaker_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u4e2d...", None))

        self.setting_speaker_button.setText(QCoreApplication.translate("MainWindow", u"\u8bd5\u97f3", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5f85\u673a(standby)\uff1a", None))
        self.setting_standby_button.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u8bdd\u672f(live_script)\uff1a", None))
        self.setting_script_button.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.setting_qa_button.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u95ee\u7b54(qa)\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u6570\u5b57\u4eba\u6a21\u578b(resource)\uff1a", None))
        self.setting_resource_button.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.setting_prebuild_button.setText(QCoreApplication.translate("MainWindow", u"\u9884\u5904\u7406 \u25b6", None))
        self.setting_standby_label.setText(QCoreApplication.translate("MainWindow", u"ok", None))
        self.setting_script_label.setText(QCoreApplication.translate("MainWindow", u"ok", None))
        self.setting_qa_label.setText(QCoreApplication.translate("MainWindow", u"ok", None))
        self.setting_resource_label.setText(QCoreApplication.translate("MainWindow", u"ok", None))
    # retranslateUi

