import re
import time
import logging

logger = logging.getLogger(__name__)


class Date:
    def __init__(self):
        self.day = self.month = self.year = None

    def from_message(self, date_str):
        self.day = int(re.split(r'\.', date_str)[0])
        self.month = int(re.split(r'\.', date_str)[1])
        self.year = int(re.split(r'\.', date_str)[2])

    def from_add_purchase(self, message):
        split = re.split(r' ', message)

        if len(split) == 3:
            self.from_message(split[1])

            if self.is_date():
                return int(split[2])

        return None

    def from_json(self, date):
        date_ = re.split(r'T', date)[0]

        self.day = int(re.split(r'-', date_)[2])
        self.month = int(re.split(r'-', date_)[1])
        self.year = int(re.split(r'-', date_)[0])

    def set_today(self):
        self.year = time.gmtime()[0]
        self.month = time.gmtime()[1]
        self.day = time.gmtime()[2]

    def is_date(self):
        if not(self.year in range(1970, 2038)):
            return False
        elif not(self.month in range(1, 12)):
            return False
        elif not(self.day in range(1, 31)):
            return False
        else:
            return True

    def get_date_key(self):
        return str(self.year) + '-' + str(self.month) + '-' + str(self.day)
