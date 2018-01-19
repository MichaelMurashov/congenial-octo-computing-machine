import json
import logging

from item import Item

logger = logging.getLogger(__name__)


class CashVoucher:
    __totalSum = 0
    __dateTime = 0  # unix time format
    __items = []

    __json_str = ""

    def get_totalsum(self):
        return self.__totalSum

    def get_datetime(self):
        return self.__dateTime

    def load(self, file_path):
        file = open(file_path, encoding='utf-8')
        self.__json_str = json.load(file)

        self.__totalSum = self.__json_str['totalSum'] / 100
        self.__dateTime = self.__json_str['dateTime']
        for buy in self.__json_str['items']:
            item = Item(buy['name'], buy['price'] / 100, buy['quantity'], buy['sum'] / 100)
            self.__items.append(item)

        logger.info('Successful parser cash voucher from file %s' % file_path)

        file.close()
