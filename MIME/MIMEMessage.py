import time
from collections import defaultdict


class MIMEMessage:
    def __init__(self):
        self.base_part = defaultdict(str)
        self.boundary = "==============={0}==".format(time.time())
        self.base_part['Content-type'] = 'multipart/mixed; boundary="{0}"'.format(self.boundary)
        self.base_part['MIME-Version'] = '1.0'
        self._attachments = []

    def add_attachment(self, attachment):
        self._validate_attachment(attachment)
        self._attachments.append(attachment)

    def as_bytes(self):
        res = self._get_mime_headers(self.base_part)
        for attachment in self._attachments:
            res += bytes("--{0}\n".format(self.boundary), encoding="utf8")
            res += self._get_mime_headers(attachment.headers)
            res += attachment.content
            res += b"\n"
        res += bytes("\n--{0}--".format(self.boundary), encoding="utf8")
        return res

    @staticmethod
    def _get_mime_headers(headers: dict):
        res = ""
        for k, v in headers.items():
            res += "{key}: {value}\n".format(key=k, value=v)
        return bytes(res+"\n", encoding="utf8")

    def _check_fields(self):
        if not self.base_part['To']:
            raise Exception("missing TO")
        if not self.base_part['From']:
            raise Exception("missing FROM")
        if not self.base_part['Subject']:
            raise Exception("missing SUBJECT")
        if not self.base_part['Date']:
            raise Exception("missing DATE")

    @staticmethod
    def _validate_attachment(attachment):
        if (attachment.headers is None
                or attachment.content is None):
                raise Exception("Invalid attachment")
