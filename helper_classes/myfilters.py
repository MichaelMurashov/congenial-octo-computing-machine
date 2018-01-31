import re
from telegram.ext import BaseFilter


class DateFilter(BaseFilter):
    def filter(self, message):
        date = re.search(r'\d{2}-|\.\d{2}-|\.\d{4}', message.text)
        return not(date is None)


class TodayFilter(BaseFilter):
    def filter(self, message):
        return 'Сегодня' in message.text


class MonthFilter(BaseFilter):
    def filter(self, message):
        return 'Месяц' in message.text


class SumFilter(BaseFilter):
    def filter(self, message):
        return 'Сумма' in message.text


class HelpFilter(BaseFilter):
    def filter(self, message):
        return 'Список команд' in message.text
