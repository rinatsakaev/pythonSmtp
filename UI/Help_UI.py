# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sendMailWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HelpWindow(object):
    def setupUi(self, helpWindow):
        helpWindow.setObjectName("helpWindow")
        helpWindow.resize(300, 400)
        self.text = QtWidgets.QTextEdit(helpWindow)
        self.text.setGeometry(QtCore.QRect(0, 0, 300, 400))
        self.text.setReadOnly(True)
        self.retranslateUi(helpWindow)
        QtCore.QMetaObject.connectSlotsByName(helpWindow)

    def retranslateUi(self, senderWindow):
        _translate = QtCore.QCoreApplication.translate
        help_text = "Server: адрес smtp сервера. Например, smtp.yandex.ru\r\n" \
                    "Port: порт сервера. Например, 465\r\n" \
                    "Login: полный адрес. Например, somelogin@yandex.ru\r\n" \
                    "TO: кому отправлять, полный адрес\r\n" \
                    "Subject: тема письма\r\n" \
                    "Body: текст письма\r\n" \
                    "Send now: отправить сейчас\r\n" \
                    "Send at: отправить в..\r\n" \
                    "Дата и время указываются в формате число.месяц часы:минуты, например 30.05 12:33\r\n" \
                    "Для прикрепления файлов нажмите кнопку Attach\r\n"
        senderWindow.setWindowTitle(_translate("helpWindow", "Help"))
        self.text.setText(_translate("helpWindow", help_text))
