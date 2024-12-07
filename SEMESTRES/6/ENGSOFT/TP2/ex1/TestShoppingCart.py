import unittest

from Item import Item
from ShoppingCart import ShoppingCart

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.shopping_cart = ShoppingCart()
        self.shopping_cart.add_item(Item("ESM", 65.0))
        self.shopping_cart.add_item(Item("GoF", 120.0))

    def test_add_item(self):
        self.shopping_cart.add_item(Item("New Item", 50.0))
        self.assertEqual(self.shopping_cart.get_item_count(), 3)
        self.assertEqual(self.shopping_cart.get_total_price(), 235.0)

    def test_remove_item(self):
        self.shopping_cart.remove_item("ESM")
        self.assertEqual(self.shopping_cart.get_item_count(), 1)
        self.assertEqual(self.shopping_cart.get_total_price(), 120.0)

    def test_get_total_price(self):
        self.assertEqual(self.shopping_cart.get_total_price(), 185.0)

    def test_clear_cart(self):
        self.shopping_cart.clear_cart()
        self.assertEqual(self.shopping_cart.get_item_count(), 0)

if __name__ == "__main__":
    unittest.main()