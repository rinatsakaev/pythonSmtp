import os
import subprocess
import unittest
from Client.MailSender import MailSender
from Client.MailSender import EmailMessage
from unittest import TestCase
from datetime import datetime
import psutil
from helpers import messages_dir, good_login, good_password, recipient


class TestMailAuthorization(TestCase):
    def setUp(self):
        self.bad_login = "brokenlogin@yandex.ru"
        self.bad_password = "brokenpassword"
        self.good_login = good_login
        self.good_password = good_password
        self.credentials = ("smtp.yandex.ru", "465")

    def test_authorization_bad(self):
        sender = MailSender(self.credentials,
                            self.bad_login,
                            self.bad_password)

        self.assertRaises(Exception, sender.__enter__)

    def test_authorization_good(self):
        sender = MailSender(self.credentials,
                            self.good_login,
                            self.good_password)
        sender.sock = sender._get_connection((self.credentials[0],
                                              int(self.credentials[1])))
        self.assertEqual(sender.authorize(), True)


class TestMailSender(TestCase):
    def setUp(self):
        self.login = good_login
        self.password = good_password
        self.credentials = ("smtp.yandex.ru", "465")
        self.msg_content = ("some subject", "some body")
        self.recipient = recipient
        self.sender = MailSender(self.credentials,
                                 self.login,
                                 self.password)

    def tearDown(self):
        self._clear_saved_messages()

    def test_simple_message(self):
        message = EmailMessage(self.login,
                               self.recipient,
                               *self.msg_content)
        try:
            with self.sender as sndr:
                sndr.send_message(message.msg)
        except Exception as e:
            self.fail(e)

    def test_attachments(self):
        message = EmailMessage(self.login,
                               self.recipient,
                               *self.msg_content,
                               ["att1.jpg"])
        try:
            with self.sender as sndr:
                sndr.send_message(message.msg)
        except Exception as e:
            self.fail(e)
        pass

    def test_save_message(self):
        message = EmailMessage(self.login,
                               self.recipient,
                               *self.msg_content)
        datetime_object = datetime.now()
        filename = MailSender.save_message(message, datetime_object)
        self.assertTrue(os.path.isfile("./"+messages_dir+"/"+filename))

    @staticmethod
    def _clear_saved_messages():
        for root, dirs, files in os.walk("./"+messages_dir):
            for filename in files:
                if filename[-3:] == "msg":
                    os.remove("./"+messages_dir+"/"+filename)


class TestDaemon(TestCase):
    def setUp(self):
        self.login = good_login
        self.password = good_password
        self.credentials = ("smtp.yandex.ru", "465")
        self.msg_content = ("some subject", "sent by daemon")
        self.recipient = recipient
        self._kill_daemons()

    def tearDown(self):
        self._kill_daemons()

    @staticmethod
    def _kill_daemons():
        if os.path.isfile("pid.tmp"):
            with open("pid.tmp", "r") as f:
                pid = int(f.read())
                if psutil.pid_exists(pid):
                    p = psutil.Process(pid)
                    p.terminate()

    def test_daemon_sending(self):
        message = EmailMessage(self.login,
                               self.recipient,
                               *self.msg_content)
        filename = MailSender.save_message(message, datetime.now())
        self.assertTrue(os.path.isfile("./"+messages_dir+"/"+filename))
        format_str = "python DaemonSender.py {0} {1} {2} {3}"
        start_string = format_str.format(self.credentials[0],
                                         self.credentials[1],
                                         self.login,
                                         self.password)
        subprocess.Popen(start_string,
                         creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        self.assertFalse(os.path.isfile(filename))


if __name__ == '__main__':
    unittest.main()
