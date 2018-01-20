import logging
import time

from helper_classes.cashvoucher import CashVoucher

logger = logging.getLogger(__name__)

'''
    Формат date_key: YYYYMMDD
    Пример: 20170130
'''
DAY = 1
WEEK = 7 * DAY
MONTH = 100
YEAR = 10000


class User:
    __id = 0
    __total_sum = 0
    __archive = {}

    def __init__(self, _id):
        self.__id = _id

    def get_id(self):
        return self.__id

    def get_totalsum(self):
        return self.__total_sum

    def clear_archive(self):
        self.__archive = {}
        self.__total_sum = 0

    def add_purchase(self, file_path):
        cash_voucher = CashVoucher()
        cash_voucher.load(file_path)

        self.__total_sum += cash_voucher.get_totalsum()

        unix_time = cash_voucher.get_datetime()
        date_key = int(time.strftime("%Y%m%d", time.localtime(unix_time)))

        if not (date_key in self.__archive):
            self.__archive[date_key] = []
        self.__archive[date_key].append(cash_voucher)

    def get_day_sum(self, date_key):
        result_sum = 0
        if date_key in self.__archive:
            cash_vouchers = self.__archive[date_key]
            for cash_voucher in cash_vouchers:
                result_sum += cash_voucher.get_totalsum()

        return result_sum

    def get_today_sum(self):
        unix_today = time.time()
        date_key = int(time.strftime("%Y%m%d", time.localtime(unix_today)))
        return self.get_day_sum(date_key)

    def get_week_sum(self):
        result_sum = 0
        unix_today = time.time()
        today = int(time.strftime("%Y%m%d", time.localtime(unix_today)))
        for i in range(WEEK):
            result_sum += self.get_day_sum(today - i)

        return result_sum
