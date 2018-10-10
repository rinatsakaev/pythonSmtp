from collections import defaultdict


class MIMEText:
    def __init__(self, text):
        self.headers = defaultdict(str)
        self.headers['MIME-Version'] = '1.0'
        self.headers['Content-Transfer-Encoding'] = '7bit'
        self.headers['Content-Type'] = 'text/plain; charset="utf8"'
        self.content = bytes(text, encoding="utf8")
