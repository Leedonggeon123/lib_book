# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_mgmt_page.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 520)
        self.user_list_tableWidget = QTableWidget(Form)
        if (self.user_list_tableWidget.columnCount() < 5):
            self.user_list_tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.user_list_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.user_list_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.user_list_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.user_list_tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.user_list_tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.user_list_tableWidget.setObjectName(u"user_list_tableWidget")
        self.user_list_tableWidget.setGeometry(QRect(10, 10, 781, 401))
        self.user_list_tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.user_list_tableWidget.setSortingEnabled(True)
        self.user_list_tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.add_user_pushButton = QPushButton(Form)
        self.add_user_pushButton.setObjectName(u"add_user_pushButton")
        self.add_user_pushButton.setGeometry(QRect(40, 440, 140, 50))
        self.edit_user_pushButton = QPushButton(Form)
        self.edit_user_pushButton.setObjectName(u"edit_user_pushButton")
        self.edit_user_pushButton.setGeometry(QRect(230, 440, 140, 50))
        self.del_user_pushButton = QPushButton(Form)
        self.del_user_pushButton.setObjectName(u"del_user_pushButton")
        self.del_user_pushButton.setGeometry(QRect(420, 440, 140, 50))
        self.cnacel_pushButton = QPushButton(Form)
        self.cnacel_pushButton.setObjectName(u"cnacel_pushButton")
        self.cnacel_pushButton.setGeometry(QRect(610, 440, 140, 50))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtablewidgetitem = self.user_list_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\uc544\uc774\ub514", None))
        ___qtablewidgetitem1 = self.user_list_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\ub4f1\uae09", None))
        ___qtablewidgetitem2 = self.user_list_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\uc774\ub984", None))
        ___qtablewidgetitem3 = self.user_list_tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\uc804\ud654\ubc88\ud638", None))
        ___qtablewidgetitem4 = self.user_list_tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\uc774\uba54\uc77c", None))
        self.add_user_pushButton.setText(QCoreApplication.translate("Form", u"\ud68c\uc6d0 \ucd94\uac00", None))
        self.edit_user_pushButton.setText(QCoreApplication.translate("Form", u"\ud68c\uc6d0 \uc218\uc815", None))
        self.del_user_pushButton.setText(QCoreApplication.translate("Form", u"\ud68c\uc6d0 \uc0ad\uc81c", None))
        self.cnacel_pushButton.setText(QCoreApplication.translate("Form", u"\ucde8\uc18c", None))
    # retranslateUi

