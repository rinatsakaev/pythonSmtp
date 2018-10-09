from datetime import datetime
from PyQt5 import QtWidgets
import MailSender
from MailSender import MailSender
from SendMail_UI import Ui_senderWindow


class SenderWindow(QtWidgets.QMainWindow):
    attachments = None

    def __init__(self, sender, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.sender = sender
        self.ui = Ui_senderWindow()
        self.ui.setupUi(self)
        self.subjectEdit = self.ui.subjectEdit
        self.bodyEdit = self.ui.bodyEdit
        self.sendStatus = self.ui.sendStatusLabel
        self.attachmentsLabel = self.ui.attachmentsLabel
        self.mailToEdit = self.ui.mailToEdit
        self.sendDate = self.ui.dateEdit
        self.ui.sendNowButton.clicked.connect(self.click_send_now)
        self.ui.addFilesButton.clicked.connect(self.click_add_files)
        self.ui.sendLaterButton.clicked.connect(self.click_send_later)

    def click_add_files(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)

        if dlg.exec_():
            self.attachments = dlg.selectedFiles()
            text = "\n".join([item.split("/")[-1]
                              for item in self.attachments])
            self.attachmentsLabel.setText(text)

    def click_send_now(self):
        message = MailSender.EmailMessage(self.sender.login,
                                          self.mailToEdit.text(),
                                          self.subjectEdit.text(),
                                          self.bodyEdit.toPlainText(),
                                          self.attachments)
        try:
            self.sender.send_message(message.msg)
            self.sendStatus.setText("OK")
        except Exception as e:
            self.sendStatus.setText(str(e))

    def click_send_later(self):
        message = MailSender.EmailMessage(self.sender.login,
                                          self.mailToEdit.text(),
                                          self.subjectEdit.text(),
                                          self.bodyEdit.toPlainText(),
                                          self.attachments)
        datetime_object = datetime.strptime(self.sendDate.text(),
                                            '%d.%m %H:%M')
        if datetime_object is None:
            self.sendStatus.setText("Bad date format. Enter %d.%m %H:%M")
        MailSender.save_message(message, datetime_object)
        self.sendStatus.setText("Saved as {0}".format(filename))
