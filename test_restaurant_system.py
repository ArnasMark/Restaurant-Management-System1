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

    def test_close_order_changes_status(self):
        pizza = FoodItem(1, "Pizza", 8.5, False)
        builder = OrderBuilder()
        order = (
            builder.set_order_id(1)
            .set_customer("Karolis")
            .set_table(2)
            .add_item(pizza, 1)
            .build()
        )
        order.close_order()
        self.assertEqual(order.status, "Closed")

    def test_total_revenue_counts_only_closed_orders(self):
        restaurant = Restaurant("Test Restaurant")
        restaurant.add_table(Table(1, 4))
        restaurant.add_table(Table(2, 4))
        pizza = FoodItem(1, "Pizza", 8.5, False)
        restaurant.add_menu_item(pizza)

        order1 = (
            OrderBuilder().set_order_id(1).set_customer("A").set_table(1).add_item(pizza, 2).build()
        )
        restaurant.create_order(order1)
        restaurant.close_order(1)

        order2 = (
            OrderBuilder().set_order_id(2).set_customer("B").set_table(2).add_item(pizza, 1).build()
        )
        restaurant.create_order(order2)

        self.assertAlmostEqual(restaurant.total_revenue(), order1.calculate_total(), places=5)
