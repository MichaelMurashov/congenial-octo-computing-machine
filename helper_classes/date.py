import re
import time
import logging

logger = logging.getLogger(__name__)


class Date:
    def __init__(self):
        self.day = self.month = self.year = None

    def from_message(self, date_str):
        self.day = re.findall(r'\d{2}', date_str)[0]
        self.month = re.findall(r'\d{2}', date_str)[1]
        self.year = re.search(r'\d{4}', date_str).group(0)

    def from_unix_format(self, unix_date):
        self.year = time.strftime("%Y", time.localtime(unix_date))
        self.month = time.strftime("%m", time.localtime(unix_date))
        self.day = time.strftime("%d", time.localtime(unix_date))

    def is_date(self):
        if not (1970 <= int(self.year) and int(self.year) <= 2038):
            return False
        elif not (1 <= int(self.month) and int(self.month) <= 12):
            return False
        elif not (1 <= int(self.day) and int(self.day) <= 31):
            return False
        else:
            return True

    def get_date_key(self):
        return int(self.year + self.month + self.day)

    def subtract_day(self):
        if int(self.day) > 1:
            string = self.get_date_key()
            day = int(string)
            day -= 1
            string = str(day)

            self.day = re.findall(r'\d{2}', string)[3]
