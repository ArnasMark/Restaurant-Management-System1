import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from restaurant_system import FoodItem, DrinkItem, OrderBuilder, Table, Restaurant


class RestaurantSystemTests(unittest.TestCase):
    def test_food_price(self):
        item = FoodItem(1, "Pizza", 8.5, False)
        self.assertEqual(item.final_price(), 8.5)

    def test_drink_price_large_size(self):
        item = DrinkItem(2, "Juice", 2.5, 750)
        self.assertEqual(item.final_price(), 3.0)

    def test_builder_creates_order(self):
        pizza = FoodItem(1, "Pizza", 8.5, False)
        builder = OrderBuilder()
        order = (
            builder.set_order_id(1)
            .set_customer("Karolis")
            .set_table(2)
            .add_item(pizza, 2)
            .set_discount(0.1)
            .build()
        )
        self.assertEqual(order.customer_name, "Karolis")
        self.assertEqual(len(order.items), 1)
