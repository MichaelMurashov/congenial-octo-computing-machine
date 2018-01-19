import logging
import time

from cashvoucher import CashVoucher

logger = logging.getLogger(__name__)


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
        key_day = time.strftime("%Y%m%d", time.localtime(unix_time))
        if not (key_day in self.__archive):
            self.__archive[key_day] = []
        self.__archive[key_day].append(cash_voucher)

        logger.info('Successful load cash voucher from file %s' % file_path)

    def get_daysum(self, unix_time):
        key_day = time.strftime("%Y%m%d", time.localtime(unix_time))

        result_sum = 0
        if key_day in self.__archive:
            cash_vouchers = self.__archive[key_day]
            for cash_voucher in cash_vouchers:
                result_sum += cash_voucher.get_totalsum()

        return result_sum
