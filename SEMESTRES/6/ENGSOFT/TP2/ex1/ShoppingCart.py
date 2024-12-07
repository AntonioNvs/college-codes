from Item import Item

from typing import List

class ShoppingCart:
    def __init__(self):
        self.__items: List[Item]  = []

    def add_item(self, item):
        self.__items.append(item)

    def remove_item(self, item_name):
        self.__items = [item for item in self.__items if item.get_name() != item_name]

    def get_total_price(self):
        return sum(item.get_price() for item in self.__items)

    def clear_cart(self):
        self.__items = []

    def get_item_count(self):
        return len(self.__items)