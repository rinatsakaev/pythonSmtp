import base64
from collections import defaultdict
from os.path import basename


class MIMEBinary:
    def __init__(self, file):
        self.headers = defaultdict(str)
        self.headers['MIME-Version'] = '1.0'
        self.headers['Content-Transfer-Encoding'] = 'base64'
        filename = basename(file)
        self.headers['Content-Type'] = 'application/octet-stream; Name="{0}"'.format(filename)
        self.headers['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
        self.content = None
        with open(file, "rb") as f:
            self.content = base64.encodebytes(f.read())