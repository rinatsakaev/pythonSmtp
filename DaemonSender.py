import sys
import time
from datetime import datetime
from os import walk
from collections import defaultdict
from email.parser import BytesFeedParser
import os
import helpers
from helpers import messages_dir
from MailSender import MailSender


class Daemon:
    def __init__(self, server_credentials: tuple, login, password):
        self.sender = MailSender(server_credentials, login, password)
        self.server_credentials = server_credentials
        self.login = login
        self.password = password
        self.msg_files = self._get_dates_to_files()

    def run(self):
        self._send_early_messages()
        while True:
            current_time = datetime.now().strftime(helpers.date_format)
            if current_time not in self.msg_files.keys():
                time.sleep(40)
                continue

            for files in self.msg_files[current_time]:
                for filename in files:
                    self._send_message(filename)

            time.sleep(40)

    def _get_dates_to_files(self) -> dict:
        dct = defaultdict(list)
        for root, dirs, files in walk("./"+messages_dir):
            for filename in files:
                dct[filename.split("_")[0]].append(filename)
        return dct

    def _send_message(self, filename):
        with open("./"+messages_dir+"/"+filename, "rb") as f:
            byte_array = bytearray(f.read())
            parser = BytesFeedParser()
            parser.feed(byte_array)
            msg = parser.close()
            self.sender.authorize()
            self.sender.send_message(msg)
            self.sender.close_connection()
        os.remove("./"+messages_dir+"/"+filename)

    def _send_early_messages(self):
        current_time = datetime.now().strftime(helpers.date_format)
        keys = [k for k in self.msg_files.keys() if k < current_time]
        for k in keys:
            for file in self.msg_files[k]:
                self._send_message(file)


if __name__ == "__main__":
    daemon = Daemon((sys.argv[1], sys.argv[2]), sys.argv[3], sys.argv[4])
    daemon.run()
