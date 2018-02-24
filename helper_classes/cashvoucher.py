import json
import logging

from helper_classes.date import Date
from helper_classes.item import Item

logger = logging.getLogger(__name__)


class CashVoucher:
    def __init__(self):
        self.total_sum = 0
        self.date_time = Date()
        self.items = []
        self.json_str = ""

    def load_from_file(self, file_path):
        file = open(file_path, encoding='utf-8')
        self.json_str = json.load(file)

        self.total_sum = self.json_str['totalSum'] / 100
        self.date_time.from_unix_format(self.json_str['dateTime'])

        for buy in self.json_str['items']:
            item = Item(buy['name'], buy['price'] / 100, buy['quantity'], buy['sum'] / 100)
            self.items.append(item)

        file.close()
