import sys
import subprocess
from PyQt5 import QtWidgets
import os
import psutil
import MailSender
from HelpWindow import HelpWindow
from Main_UI import Ui_MainWindow
from SenderWindow import SenderWindow


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
            return False
        return True

    def click_authorize(self):
        if not self.check_fields():
            self.authorizationStatus.setText("Fill all the fields")
            return

        self.sender = MailSender.MailSender((self.serverEdit.text(),
                                             self.portEdit.text()),
                                            self.loginEdit.text(),
                                            self.passwordEdit.text())
        self.close()
        self.sender.sock = self.sender._get_connection((self.serverEdit.text(),
                                                        int(self.portEdit.text())))
        if self.sender.authorize():
            self.senderWindow = SenderWindow(self.sender)
            self.senderWindow.show()
            self.start_daemon()

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

