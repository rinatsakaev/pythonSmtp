import subprocess
from PyQt5 import QtWidgets
import os
import psutil
from Client import MailSender
from Windows.HelpWindow import HelpWindow
from UI.Main_UI import Ui_MainWindow
from Windows.SenderWindow import SenderWindow
from socket import gaierror

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.sender = None
        self.senderWindow = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.serverEdit = self.ui.serverEdit
        self.portEdit = self.ui.portEdit
        self.loginEdit = self.ui.loginEdit
        self.passwordEdit = self.ui.passwordEdit
        self.authorizationStatus = self.ui.authorizeStatusLabel
        self.ui.authorizeButton.clicked.connect(self.click_authorize)
        self.ui.helpButton.clicked.connect(self.click_help)

    def check_fields(self):
        """
        Validates user input
        :return:
        """
        if (self.serverEdit.text() == "" or
           self.portEdit.text() == "" or
           self.loginEdit.text() == "" or
           self.passwordEdit.text() == ""):
            return "Fill all the fields"
        try:
            port = int(self.portEdit.text())
            if port > 65535 or port <= 0:
                return "Port should be >0 and <=65535"
        except Exception:
            return "Port should be integer"
        return None

    def click_authorize(self):
        authorization_result = self.check_fields()
        if authorization_result is not None:
            self.authorizationStatus.setText(authorization_result)
            return
        try:
            self.sender = MailSender.MailSender((self.serverEdit.text(),
                                                 self.portEdit.text()),
                                                self.loginEdit.text(),
                                                self.passwordEdit.text())
            self.sender.sock = self.sender._get_connection((self.serverEdit.text(),
                                                            int(self.portEdit.text())))
            if self.sender.authorize():
                self.close()
                self.senderWindow = SenderWindow(self.sender)
                self.senderWindow.show()
                self.start_daemon()
            else:
                self.authorizationStatus.setText("Wrong login or password")
        except gaierror:
            self.authorizationStatus.setText("Can't connect to server")

    def start_daemon(self):
        format_str = "python DaemonSender.py {0} {1} {2} {3}"
        start_string = format_str.format(self.sender.server_credentials[0],
                                         self.sender.server_credentials[1],
                                         self.sender.login,
                                         self.sender.password)
        if os.path.isfile("pid.tmp"):
            with open("pid.tmp", "r") as f:
                pid = int(f.read())
                if psutil.pid_exists(pid):
                    cmd_string = " ".join(psutil.Process(pid).cmdline())
                    start_index = cmd_string.index("DaemonSender.py")
                    cmd_string = cmd_string[start_index:]
                    if cmd_string == start_string[7:]:
                        return

        process = subprocess.Popen(start_string,
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

        with open("pid.tmp", "w") as f:
            f.write(str(process.pid))

    def click_help(self):
        self.helpWindow = HelpWindow()
        self.helpWindow.show()