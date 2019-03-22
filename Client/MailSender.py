import logging
import os
from socket import *
from base64 import *
import time
import ssl
from datetime import datetime
from MIME.MIMEMessage import MIMEMessage
from MIME.MIMEBinary import MIMEBinary
from MIME.MIMEText import MIMEText
from helpers import date_format, messages_dir, mime_time_format
from socket import gaierror

class EmailMessage:
    """
    Class for constructing EmailMessage data
    """
    def __init__(self, email_from, email_to, subject, body, attachments=None):
        self.msg = MIMEMessage()
        self.msg.base_part['From'] = email_from
        self.msg.base_part['To'] = email_to
        self.msg.base_part['Subject'] = subject
        self.msg.base_part['Date'] = time.strftime(mime_time_format, time.gmtime())
        self.logger = logging.getLogger()
        body = MIMEText(body)
        self.msg.add_attachment(body)
        if attachments is not None:
            for file in attachments:
                self.msg.add_attachment(MIMEBinary(file))


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
        self._is_authorized = False

    def __enter__(self):
        if self.sock is None:
            self.sock = self._get_connection(self.server_credentials)
        if not self._is_authorized:
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
            return False
        self._is_authorized = True
        return True

    def send_message(self, message):
        """
        Sends DATA to server
        :param message:
        :return:
        """
        mail_from_msg = "MAIL FROM:{0}\r\n".format(message.base_part['From'])
        mail_to_msg = "RCPT TO:{0}\r\n".format(message.base_part['To'])
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
        except gaierror as e:
            logging.exception(e)
            raise

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
