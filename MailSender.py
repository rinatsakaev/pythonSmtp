import logging
import os
from cgi import log
from socket import *
from base64 import *
import time
import ssl
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from helpers import date_format, messages_dir, mime_time_format


class EmailMessage:
    """
    Class for constructing EmailMessage data
    """
    def __init__(self, email_from, email_to, subject, body, attachments=None):
        self.msg = MIMEMultipart()
        self.msg['From'] = email_from
        self.msg['To'] = email_to
        self.msg['Subject'] = subject
        self.msg['Date'] = time.strftime(mime_time_format, time.gmtime())
        self.logger = logging.getLogger()
        text = MIMEText(body)
        MIMEText.set_charset(text, "utf8")
        self.msg.attach(text)
        if attachments is not None:
            for file in attachments:
                with open(file, "rb") as f:
                    part_content = MIMEApplication(f.read(),
                                                   Name=basename(file))
                part_content['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
                self.msg.attach(part_content)


class MailSender:
    """
    Class for sending email messages via SMTP
    """
    def __init__(self, server_credentials: tuple, login, password):
        self.server_credentials = (server_credentials[0],
                                   int(server_credentials[1]))
        self.login = login
        self.password = password
        self.sock = None

    def __enter__(self):
        self.sock = self._get_connection(self.server_credentials)
        self.authorize()
        return self

    def __exit__(self, *args):
        self._close_connection()

    def authorize(self):
        """
        Tries to authorize user on server with given credentials.
        Returns True if authorized
        :return:
        """
        self.sock.send(b"EHLO user\r\n")
        self.sock.recv(1024)
        base64_str = "\x00{0}\x00{1}".format(self.login, self.password).encode()
        base64_bytes = b64encode(base64_str)
        auth_msg = b''.join([b"AUTH PLAIN ", base64_bytes, b"\r\n"])
        self.sock.send(auth_msg)
        recv_auth = self.sock.recv(1024)
        if not recv_auth.decode().split(' ')[0] == "235":
            raise Exception(recv_auth.decode())
        return True

    def send_message(self, message: MIMEMultipart):
        """
        Sends DATA to server
        :param message:
        :return:
        """
        mail_from_msg = "MAIL FROM:{0}\r\n".format(message['From'])
        mail_to_msg = "RCPT TO:{0}\r\n".format(message['To'])
        self._send_command(mail_from_msg, 250)
        self._send_command(mail_to_msg, 250)
        self._send_command("DATA\r\n", 354)
        self.sock.send(message.as_bytes())
        self._send_command("\r\n.\r\n", 250)

    def _send_command(self, command, expected_response_code):
        """
        Sends command to server, throws exception if response code is wrong
        :param command:
        :param expected_response_code:
        :return:
        """
        self.sock.send(command.encode())
        response = self.sock.recv(1024).decode()
        logging.info(response)
        if response.split(' ')[0] != str(expected_response_code):
            raise Exception(response)

    def _get_connection(self, addr):
        """
        Tries to establish ssl connection with a server. Else throws exception.
        :param addr:
        :return:
        """
        sock = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM))
        try:
            sock.connect(addr)
            sock.recv(1024)
            return sock
        except Exception as e:
            logging.exception(e)

    def _close_connection(self):
        self.sock.send("QUIT".encode())
        self.sock.close()

    @staticmethod
    def save_message(message, datetime_object):
        filename = "{0}_{1}.msg".format(
            datetime_object.strftime(date_format),
            str(datetime.timestamp(datetime.now())))
        if not os.path.isdir(messages_dir):
            os.makedirs(messages_dir)
        with open("./"+messages_dir+"/"+filename, "wb") as f:
            f.write(message.msg.as_bytes())
        return filename
