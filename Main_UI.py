# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'authorizeWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(356, 344)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.authorizeButton = QtWidgets.QPushButton(self.centralwidget)
        self.authorizeButton.setGeometry(QtCore.QRect(110, 200, 141, 61))
        self.authorizeButton.setObjectName("authorizeButton")
        self.serverEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.serverEdit.setGeometry(QtCore.QRect(110, 30, 141, 20))
        self.serverEdit.setObjectName("serverEdit")
        self.portEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.portEdit.setGeometry(QtCore.QRect(110, 70, 141, 20))
        self.portEdit.setObjectName("portEdit")
        self.loginEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.loginEdit.setGeometry(QtCore.QRect(110, 110, 141, 20))
        self.loginEdit.setObjectName("loginEdit")
        self.passwordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordEdit.setGeometry(QtCore.QRect(110, 150, 141, 20))
        self.passwordEdit.setObjectName("passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 46, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 46, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 46, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 61, 16))
        self.label_4.setObjectName("label_4")
        self.authorizeStatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.authorizeStatusLabel.setGeometry(QtCore.QRect(30, 270, 301, 41))
        self.authorizeStatusLabel.setObjectName("authorizeStatusLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 356, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.authorizeButton.setText(_translate("MainWindow", "Authorize"))
        self.label.setText(_translate("MainWindow", "Server"))
        self.label_2.setText(_translate("MainWindow", "Port"))
        self.label_3.setText(_translate("MainWindow", "Login"))
        self.label_4.setText(_translate("MainWindow", "Password"))
        self.authorizeStatusLabel.setText(_translate("MainWindow", ""))
