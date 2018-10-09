# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sendMailWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_senderWindow(object):
    def setupUi(self, senderWindow):
        senderWindow.setObjectName("senderWindow")
        senderWindow.resize(827, 595)
        self.mailToEdit = QtWidgets.QLineEdit(senderWindow)
        self.mailToEdit.setGeometry(QtCore.QRect(90, 30, 141, 20))
        self.mailToEdit.setObjectName("mailToEdit")
        self.subjectEdit = QtWidgets.QLineEdit(senderWindow)
        self.subjectEdit.setGeometry(QtCore.QRect(90, 70, 481, 20))
        self.subjectEdit.setObjectName("subjectEdit")
        self.bodyEdit = QtWidgets.QPlainTextEdit(senderWindow)
        self.bodyEdit.setGeometry(QtCore.QRect(90, 120, 631, 311))
        self.bodyEdit.setObjectName("bodyEdit")
        self.sendNowButton = QtWidgets.QPushButton(senderWindow)
        self.sendNowButton.setGeometry(QtCore.QRect(90, 460, 451, 51))
        self.sendNowButton.setObjectName("sendNowButton")
        self.addFilesButton = QtWidgets.QPushButton(senderWindow)
        self.addFilesButton.setGeometry(QtCore.QRect(570, 460, 75, 23))
        self.addFilesButton.setObjectName("addFilesButton")
        self.sendLaterButton = QtWidgets.QPushButton(senderWindow)
        self.sendLaterButton.setGeometry(QtCore.QRect(90, 530, 181, 23))
        self.sendLaterButton.setObjectName("sendLaterButton")
        self.attachmentsLabel = QtWidgets.QLabel(senderWindow)
        self.attachmentsLabel.setGeometry(QtCore.QRect(660, 460, 151, 91))
        self.attachmentsLabel.setText("")
        self.attachmentsLabel.setObjectName("attachmentsLabel")
        self.sendStatusLabel = QtWidgets.QLabel(senderWindow)
        self.sendStatusLabel.setGeometry(QtCore.QRect(90, 570, 441, 41))
        self.sendStatusLabel.setText("")
        self.sendStatusLabel.setObjectName("sendStatusLabel")
        self.label = QtWidgets.QLabel(senderWindow)
        self.label.setGeometry(QtCore.QRect(20, 30, 46, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(senderWindow)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 61, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(senderWindow)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 61, 20))
        self.label_3.setObjectName("label_3")
        self.dateEdit = QtWidgets.QLineEdit(senderWindow)
        self.dateEdit.setGeometry(QtCore.QRect(280, 530, 141, 20))
        self.dateEdit.setPlaceholderText("%d.%m %H:%M")
        self.dateEdit.setObjectName("dateEdit")

        self.retranslateUi(senderWindow)
        QtCore.QMetaObject.connectSlotsByName(senderWindow)

    def retranslateUi(self, senderWindow):
        _translate = QtCore.QCoreApplication.translate
        senderWindow.setWindowTitle(_translate("senderWindow", "Form"))
        self.sendNowButton.setText(_translate("senderWindow", "Send now"))
        self.addFilesButton.setText(_translate("senderWindow", "Attach"))
        self.sendLaterButton.setText(_translate("senderWindow", "Send at:"))
        self.label.setText(_translate("senderWindow", "TO:"))
        self.label_2.setText(_translate("senderWindow", "Subject:"))
        self.label_3.setText(_translate("senderWindow", "Body:"))
