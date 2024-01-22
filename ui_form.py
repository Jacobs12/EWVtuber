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
        self.stackedWidget.setGeometry(QRect(130, 0, 681, 601))
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
        self.label_2.setGeometry(QRect(35, 90, 58, 16))
        self.setting_speaker_combo = QComboBox(self.page)
        self.setting_speaker_combo.addItem("")
        self.setting_speaker_combo.setObjectName(u"setting_speaker_combo")
        self.setting_speaker_combo.setGeometry(QRect(106, 80, 221, 32))
        self.pushButton_2 = QPushButton(self.page)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(350, 80, 100, 32))
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

        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u8bd5\u97f3", None))
    # retranslateUi

