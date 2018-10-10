import time
import unittest
from unittest import TestCase
from MIME.MIMEMessage import MIMEMessage
from MIME.MIMEText import MIMEText
from MIME.MIMEBinary import MIMEBinary
from helpers import mime_time_format
import re


class TestMime(TestCase):
    def test_simple_mime(self):
        mime = MIMEMessage()
        mime.base_part['From'] = "r.sakaevv@gmail.com"
        mime.base_part['To'] = "r-sakaevv@yandex.ru"
        mime.base_part['Subject'] = "some subject"
        mime.base_part['Date'] = time.strftime(mime_time_format, time.gmtime())
        mime.add_attachment(MIMEText("hello world"))
        correct_result = b"""Content-type: multipart/mixed; boundary=""\nMIME-Version: 1.0\nFrom: r.sakaevv@gmail.com\nTo: r-sakaevv@yandex.ru\nSubject: some subject\nDate: \n\n---\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nContent-Type: text/plain; charset="utf8"\n\nhello world"""
        result = self._crop_dynamic_fields(mime.as_bytes())
        self.assertEqual(correct_result, result)

    def test_attachments_mime(self):
        mime = MIMEMessage()
        mime.base_part['From'] = "r.sakaevv@gmail.com"
        mime.base_part['To'] = "r-sakaevv@yandex.ru"
        mime.base_part['Subject'] = "some subject"
        mime.base_part['Date'] = time.strftime(mime_time_format, time.gmtime())
        mime.add_attachment(MIMEBinary("att1.jpg"))
        correct_result = b"""Content-type: multipart/mixed; boundary=""\nMIME-Version: 1.0\nFrom: r.sakaevv@gmail.com\nTo: r-sakaevv@yandex.ru\nSubject: some subject\nDate: \n\n---\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nContent-Type: application/octet-stream; Name="att1.jpg"\nContent-Disposition: attachment; filename="att1.jpg"\n\n/9j/4AAQSkZJRgABAQEASABIAAD//gBbRmlsZSBzb3VyY2U6IGh0dHA6Ly9ydS53aWtpcGVkaWEu\nb3JnL3dpa2kvJUQwJUE0JUQwJUIwJUQwJUI5JUQwJUJCOk9yaWdpbmFsX0RvZ2VfbWVtZS5qcGf/\n2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSop\nGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgo\nKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCADfASwDASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAA\nAAAAAAAABAECAwUGAAcI/8QAPxAAAQMDAgQEAwYFAwMEAwAAAQIDEQAEIRIxBUFRYQYTInGBkaEU\nMkKxwfAHI1LR4RVi8RYzgiRTcqIlQ2P/xAAaAQACAwEBAAAAAAAAAAAAAAABAwACBAUG/8QAKREA\nAgICAwACAgIBBQEAAAAAAAECEQMSBCExE0EiUQVhFCMyQlJxsf/aAAwDAQACEQMRAD8A8gv7yxQl\nh1haS+tzW2gGCCTien9qj8VXF/Z8THDuK8S+2LtwHQpKtQQVCdM7yJj41j2kBSv0o5LYCTIkn86S\nsfdk86LJi+atmnnGUBx5SNAUoSEzzoq844/xW1tGbhDSDaJKUuITpkfuKzJccYdJbIE7iN6uOE2h\n4ostWyFh7SV6EiZA3NVnjjezDZovCV69ecTsxePrcSyFaZySPfny+le2eFrlbzyQ8nXOQpXIV4v4\nK4ZcI4k45rhIRp64POvZuAPtW5ZDhHpAAA5iK4H8lq8io1YItRs2ibtAWUExFHWzzbyNSJjlWXuu\nIMumUoAAPKktOIuIdSNRifhXLllSdGhQ6NcpKDsc1GXAk4INVirvUncT703zySZJ7dqEsioKRYqu\nYFRG7cJxQqFpI0qMGniBz2pcsl+Fkh1w+8UgJmT0pbRguK1OKJPQ0wuhCTEmuW+W2ZH3ulKc47W2\nWSdE/E7lLLTaE8ycRQIdIzMGjUWIfDSn9XoRMEzk0dbcIYV63EkzsDSsscs8nXheLjFdlI+0TcNO\nhJIUMmrG2EaTvVD4jfXw+7acaSYnI6jmI5CtBZFLqGlNmUqAIPWuxxJf8H6hWWFLb9mgbH8sY5U/\n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\n"""
        result = self._crop_dynamic_fields(mime.as_bytes())
        self.assertEqual(correct_result, result)

    @staticmethod
    def _crop_dynamic_fields(msg: bytes):
        msg_str = msg.decode("utf-8")
        reg_exp_boundary = '.*?boundary="(.*?)"'
        reg_exp_date = '.*?Date:.?(.*?)\n'
        boundary = re.match(reg_exp_boundary, msg_str).group(1)
        msg_str = msg_str.replace(boundary, "")
        date = re.match(reg_exp_date, msg_str, flags=re.DOTALL).group(1)
        msg_str = msg_str.replace(date, "")
        return bytes(msg_str, encoding="utf8")


if __name__ == '__main__':
    unittest.main()
