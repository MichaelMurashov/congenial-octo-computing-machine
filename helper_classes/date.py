import re


class Date:
    def __init__(self, date):
        self.__day = re.findall(r'\d{2}', date)[0]
        self.__month = re.findall(r'\d{2}', date)[1]
        self.__year = re.search(r'\d{4}', date).group(0)

    def check_date(self):
        if not (1970 <= int(self.__year) and int(self.__year) <= 2068):
            return False
        elif not (1 <= int(self.__month) and int(self.__month) <= 12):
            return False
        elif not (1 <= int(self.__day) and int(self.__day) <= 31):
            return False
        else:
            return True

    def get_date_key(self):
        return int(str(self.__year) + str(self.__month) + str(self.__day))
