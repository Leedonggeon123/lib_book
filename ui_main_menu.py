# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #D2B48C,\n"
"    stop: 1 #C8A97E\n"
");")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: white;")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 800, 80))
        self.frame.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #F3E6DB,\n"
"    stop: 1 #E5D0C0\n"
");\n"
"color: black;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.btn_exit = QPushButton(self.frame)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(650, 10, 121, 61))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.btn_exit.setFont(font)
        self.btn_exit.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #5E3023,\n"
"    stop: 1 #8B5A4A\n"
");\n"
"color: white;\n"
"border-radius: 30px;\n"
"text-align: center;")
        self.btn_logout = QPushButton(self.frame)
        self.btn_logout.setObjectName(u"btn_logout")
        self.btn_logout.setGeometry(QRect(520, 10, 121, 61))
        self.btn_logout.setFont(font)
        self.btn_logout.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #5E3023,\n"
"    stop: 1 #8B5A4A\n"
");\n"
"color: white;\n"
"border-radius: 30px;\n"
"text-align: center;")
        self.lbl_title = QLabel(self.frame)
        self.lbl_title.setObjectName(u"lbl_title")
        self.lbl_title.setGeometry(QRect(40, 20, 171, 41))
        self.lbl_title.setFont(font)
        self.lbl_title.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #5E3023,\n"
"    stop: 1 #8B5A4A\n"
");\n"
"color: white;\n"
"border-radius: 30px;\n"
"text-align: center;")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_user_icon = QPushButton(self.frame)
        self.lbl_user_icon.setObjectName(u"lbl_user_icon")
        self.lbl_user_icon.setGeometry(QRect(354, 15, 161, 50))
        self.lbl_user_icon.setFont(font)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 80, 800, 520))
        self.stackedWidget.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #D2B48C,\n"
"    stop: 1 #C8A97E\n"
");")
        self.main_page = QWidget()
        self.main_page.setObjectName(u"main_page")
        self.label_gif = QLabel(self.main_page)
        self.label_gif.setObjectName(u"label_gif")
        self.label_gif.setGeometry(QRect(0, 0, 800, 537))
        self.label_gif.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #D2B48C,\n"
"    stop: 1 #C8A97E\n"
");")
        self.label_gif.setPixmap(QPixmap(u":/newPrefix/ui_data/library_animation.gif"))
        self.label_gif.setScaledContents(True)
        self.btn_manage_user = QPushButton(self.main_page)
        self.btn_manage_user.setObjectName(u"btn_manage_user")
        self.btn_manage_user.setGeometry(QRect(360, 370, 161, 61))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.btn_manage_user.setFont(font1)
        self.btn_manage_user.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #836953,\n"
"    stop: 1 #A58B78\n"
");\n"
"color: white;")
        self.btn_check_rent = QPushButton(self.main_page)
        self.btn_check_rent.setObjectName(u"btn_check_rent")
        self.btn_check_rent.setGeometry(QRect(560, 50, 161, 61))
        self.btn_check_rent.setFont(font1)
        self.btn_check_rent.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #836953,\n"
"    stop: 1 #A58B78\n"
");\n"
"color: white;")
        self.btn_rent = QPushButton(self.main_page)
        self.btn_rent.setObjectName(u"btn_rent")
        self.btn_rent.setGeometry(QRect(140, 50, 161, 61))
        font2 = QFont()
        font2.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font2.setPointSize(16)
        font2.setBold(True)
        self.btn_rent.setFont(font2)
        self.btn_rent.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #836953,\n"
"    stop: 1 #A58B78\n"
");\n"
"color: white;")
        self.btn_rent_list = QPushButton(self.main_page)
        self.btn_rent_list.setObjectName(u"btn_rent_list")
        self.btn_rent_list.setGeometry(QRect(140, 220, 161, 61))
        self.btn_rent_list.setFont(font1)
        self.btn_rent_list.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #836953,\n"
"    stop: 1 #A58B78\n"
");\n"
"color: white;")
        self.btn_manage_book = QPushButton(self.main_page)
        self.btn_manage_book.setObjectName(u"btn_manage_book")
        self.btn_manage_book.setGeometry(QRect(560, 210, 161, 61))
        self.btn_manage_book.setFont(font1)
        self.btn_manage_book.setStyleSheet(u"background: qlineargradient(\n"
"    x1: 0, y1: 0,\n"
"    x2: 1, y2: 1,\n"
"    stop: 0 #836953,\n"
"    stop: 1 #A58B78\n"
");\n"
"color: white;")
        self.stackedWidget.addWidget(self.main_page)
        self.label_gif.raise_()
        self.btn_manage_user.raise_()
        self.btn_rent_list.raise_()
        self.btn_rent.raise_()
        self.btn_manage_book.raise_()
        self.btn_check_rent.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.raise_()
        self.frame.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"\uc885\ub8cc ", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8\uc544\uc6c3 ", None))
        self.lbl_title.setText(QCoreApplication.translate("MainWindow", u"\U0000b3c4\U0000c11c\U0000ad00 \U0001f4d8", None))
        self.lbl_user_icon.setText(QCoreApplication.translate("MainWindow", u"[\ub4f1\uae09] \uc0ac\uc6a9\uc790ID", None))
        self.label_gif.setText("")
        self.btn_manage_user.setText(QCoreApplication.translate("MainWindow", u"\ud68c\uc6d0\uad00\ub9ac ", None))
        self.btn_check_rent.setText(QCoreApplication.translate("MainWindow", u"\ub300\uc5ec\ud655\uc778 ", None))
        self.btn_rent.setText(QCoreApplication.translate("MainWindow", u"\ub3c4\uc11c\ub300\uc5ec ", None))
        self.btn_rent_list.setText(QCoreApplication.translate("MainWindow", u"\ub300\uc5ec\ubaa9\ub85d ", None))
        self.btn_manage_book.setText(QCoreApplication.translate("MainWindow", u"\ub3c4\uc11c\uad00\ub9ac ", None))
    # retranslateUi

