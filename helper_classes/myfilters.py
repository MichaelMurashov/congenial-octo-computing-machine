import re
from telegram.ext import BaseFilter


class DateFilter(BaseFilter):
    def filter(self, message):
        date = re.search(r'\d{2}-|\.\d{2}-|\.\d{4}', message.text)
        return not(date is None)


class TodayFilter(BaseFilter):
    def filter(self, message):
        return 'Сегодня' in message.text


class WeekFilter(BaseFilter):
    def filter(self, message):
        return 'Неделя' in message.text


class MonthFilter(BaseFilter):
    def filter(self, message):
        return 'Месяц' in message.text


class YearFilter(BaseFilter):
    def filter(self, message):
        return 'Год' in message.text
