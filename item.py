class Item:
    def __init__(self, name, price, quantity, sum):
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__sum = sum

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def get_sum(self):
        return self.__sum
