import json
import os
from abc import ABC, abstractmethod
from typing import List


class MenuItem(ABC):
    def __init__(self, item_id: int, name: str, price: float):
        if item_id <= 0:
            raise ValueError("Item ID must be positive.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.item_id = item_id
        self.name = name.strip()
        self.price = price

    @abstractmethod
    def final_price(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def item_type(self) -> str:
        raise NotImplementedError

    def __str__(self):
        return f"{self.item_id}. {self.name} | {self.item_type()} | {self.final_price():.2f} EUR"

class FoodItem(MenuItem):
    def __init__(self, item_id: int, name: str, price: float, vegan: bool = False):
        super().__init__(item_id, name, price)
        self.vegan = vegan

    def final_price(self) -> float:
        return self.price

    def item_type(self) -> str:
        return "Food"

    def __str__(self):
        vegan_text = " | Vegan" if self.vegan else ""
        return f"{super().__str__()}{vegan_text}"


class DrinkItem(MenuItem):
    def __init__(self, item_id: int, name: str, price: float, size_ml: int):
        super().__init__(item_id, name, price)
        if size_ml <= 0:
            raise ValueError("Drink size must be positive.")
        self.size_ml = size_ml

    def final_price(self) -> float:
        if self.size_ml > 500:
            return self.price + 0.50
        return self.price

    def item_type(self) -> str:
        return "Drink"

    def __str__(self):
        return f"{super().__str__()} | {self.size_ml} ml"


class OrderItem:
    def __init__(self, menu_item: MenuItem, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.menu_item = menu_item
        self.quantity = quantity

    def subtotal(self) -> float:
        return self.menu_item.final_price() * self.quantity


class Order:
    def __init__(self, order_id: int, customer_name: str, table_number: int):
        if order_id <= 0:
            raise ValueError("Order ID must be positive.")
        if not customer_name.strip():
            raise ValueError("Customer name cannot be empty.")
        self.order_id = order_id
        self.customer_name = customer_name.strip()
        self.table_number = table_number
        self.items: List[OrderItem] = []
        self.discount = 0.0
        self.service_fee = 0.10
        self.status = "Open"

    def add_item(self, menu_item: MenuItem, quantity: int):
        if self.status == "Closed":
            raise ValueError("Cannot modify closed order.")
        self.items.append(OrderItem(menu_item, quantity))

    def calculate_total(self) -> float:
        subtotal = sum(item.subtotal() for item in self.items)
        total = subtotal * (1 - self.discount)
        total += total * self.service_fee
        return total

    def close_order(self):
        if not self.items:
            raise ValueError("Cannot close empty order.")
        self.status = "Closed"

    def __str__(self):
        return (
            f"Order #{self.order_id} | Customer: {self.customer_name} | "
            f"Table: {self.table_number} | Status: {self.status} | "
            f"Total: {self.calculate_total():.2f} EUR"
        )

class OrderBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._order_id = None
        self._customer_name = None
        self._table_number = None
        self._items = []
        self._discount = 0.0

    def set_order_id(self, order_id: int):
        self._order_id = order_id
        return self

    def set_customer(self, customer_name: str):
        self._customer_name = customer_name
        return self

    def set_table(self, table_number: int):
        self._table_number = table_number
        return self

    def add_item(self, menu_item: MenuItem, quantity: int):
        self._items.append((menu_item, quantity))
        return self

    def set_discount(self, discount: float):
        if discount < 0 or discount > 1:
            raise ValueError("Discount must be between 0 and 1.")
        self._discount = discount
        return self

    def build(self) -> Order:
        if self._order_id is None:
            raise ValueError("Order ID must be set.")
        if self._customer_name is None:
            raise ValueError("Customer name must be set.")
        if self._table_number is None:
            raise ValueError("Table number must be set.")
        order = Order(self._order_id, self._customer_name, self._table_number)
        for item, quantity in self._items:
            order.add_item(item, quantity)
        order.discount = self._discount
        self.reset()
        return order


class Table:
    def __init__(self, table_number: int, seats: int):
        if table_number <= 0:
            raise ValueError("Table number must be positive.")
        if seats <= 0:
            raise ValueError("Seats must be positive.")
        self.table_number = table_number
        self.seats = seats
        self.is_reserved = False

    def reserve(self):
        if self.is_reserved:
            raise ValueError("Table already reserved.")
        self.is_reserved = True

    def free(self):
        self.is_reserved = False

    def __str__(self):
        return f"Table {self.table_number} | Seats: {self.seats} | Reserved: {self.is_reserved}"


class Restaurant:
    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Restaurant name cannot be empty.")
        self.name = name.strip()
        self.menu: List[MenuItem] = []
        self.orders: List[Order] = []
        self.tables: List[Table] = []

    def add_menu_item(self, item: MenuItem):
        if any(existing.item_id == item.item_id for existing in self.menu):
            raise ValueError("Menu item with this ID already exists.")
        self.menu.append(item)

    def remove_menu_item(self, item_id: int):
        item = self.find_menu_item(item_id)
        if item is None:
            raise ValueError("Menu item not found.")
        self.menu.remove(item)

    def find_menu_item(self, item_id: int):
        for item in self.menu:
            if item.item_id == item_id:
                return item
        return None

    def show_menu(self):
        print("\n=== MENU ===")
        if not self.menu:
            print("Menu is empty.")
            return
        for item in self.menu:
            print(item)

    def add_table(self, table: Table):
        if any(existing.table_number == table.table_number for existing in self.tables):
            raise ValueError("Table already exists.")
        self.tables.append(table)

    def show_tables(self):
        print("\n=== TABLES ===")
        if not self.tables:
            print("No tables found.")
            return
        for table in self.tables:
            print(table)

    def find_table(self, table_number: int):
        for table in self.tables:
            if table.table_number == table_number:
                return table
        return None

    def reserve_table_manually(self, table_number: int):
        table = self.find_table(table_number)
        if table is None:
            raise ValueError("Table not found.")
        table.reserve()

    def free_table_manually(self, table_number: int):
        table = self.find_table(table_number)
        if table is None:
            raise ValueError("Table not found.")
        table.free()

    def create_order(self, order: Order):
        table = self.find_table(order.table_number)
        if table is None:
            raise ValueError("Table not found.")
        if table.is_reserved:
            raise ValueError("Table is already reserved.")
        table.reserve()
        self.orders.append(order)

    def show_orders(self):
        print("\n=== ORDERS ===")
        if not self.orders:
            print("No orders found.")
            return
        for order in self.orders:
            print(order)
            for item in order.items:
                print(f"  - {item.menu_item.name} x{item.quantity} = {item.subtotal():.2f} EUR")

    def close_order(self, order_id: int):
        for order in self.orders:
            if order.order_id == order_id:
                order.close_order()
                table = self.find_table(order.table_number)
                if table:
                    table.free()
                print("Order closed successfully.")
                return
        raise ValueError("Order not found.")

    def total_revenue(self) -> float:
        return sum(order.calculate_total() for order in self.orders if order.status == "Closed")

    def save_orders(self, filename: str):
        data = []
        for order in self.orders:
            data.append({
                "order_id": order.order_id,
                "customer_name": order.customer_name,
                "table_number": order.table_number,
                "status": order.status,
                "discount": order.discount,
                "service_fee": order.service_fee,
                "total": order.calculate_total(),
                "items": [
                    {
                        "item_id": item.menu_item.item_id,
                        "item_name": item.menu_item.name,
                        "quantity": item.quantity,
                        "subtotal": item.subtotal()
                    }
                    for item in order.items
                ]
            })
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Data saved successfully.")
        
    def load_orders(self, filename: str):
        if not os.path.exists(filename):
            print("Data file not found. Starting fresh.")
            return

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.orders.clear()

        for order_data in data:
            order = Order(
                order_data["order_id"],
                order_data["customer_name"],
                order_data["table_number"]
            )
            order.discount = order_data["discount"]
            order.service_fee = order_data["service_fee"]

            for item_data in order_data["items"]:
                menu_item = self.find_menu_item(item_data["item_id"])
                if menu_item:
                    order.add_item(menu_item, item_data["quantity"])

            order.status = order_data["status"]
            self.orders.append(order)

        print("Orders loaded.")

    def clear_orders(self, filename: str):
        self.orders.clear()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

        print("All orders cleared.")

def load_default_data(restaurant: Restaurant):
    restaurant.add_table(Table(1, 4))
    restaurant.add_table(Table(2, 2))
    restaurant.add_table(Table(3, 6))
    restaurant.add_menu_item(FoodItem(1, "Pizza", 8.50, False))
    restaurant.add_menu_item(FoodItem(2, "Vegan Salad", 6.20, True))
    restaurant.add_menu_item(DrinkItem(3, "Cola", 2.00, 500))
    restaurant.add_menu_item(DrinkItem(4, "Orange Juice", 2.50, 750))

def add_menu_item_ui(restaurant: Restaurant):
    try:
        item_type = input("Enter type (food/drink): ").strip().lower()
        item_id = int(input("Item ID: "))
        name = input("Name: ").strip()
        price = float(input("Price: "))
        if item_type == "food":
            vegan = input("Is vegan? (y/n): ").strip().lower() == "y"
            item = FoodItem(item_id, name, price, vegan)
        elif item_type == "drink":
            size_ml = int(input("Size in ml: "))
            item = DrinkItem(item_id, name, price, size_ml)
        else:
            print("Invalid item type.")
            return
        restaurant.add_menu_item(item)
        print("Menu item added successfully.")
    except Exception as error:
        print("Error:", error)

def remove_menu_item_ui(restaurant: Restaurant):
    try:
        item_id = int(input("Enter menu item ID to remove: "))
        restaurant.remove_menu_item(item_id)
        print("Menu item removed successfully.")
    except Exception as error:
        print("Error:", error)

def create_order_ui(restaurant: Restaurant):
    try:
        order_id = int(input("Order ID: "))
        customer_name = input("Customer name: ").strip()
        table_number = int(input("Table number: "))
        discount_percent = float(input("Discount % (0 if none): "))

        builder = OrderBuilder()
        builder.set_order_id(order_id)
        builder.set_customer(customer_name)
        builder.set_table(table_number)
        builder.set_discount(discount_percent / 100)

        while True:
            restaurant.show_menu()
            item_id = int(input("Enter menu item ID (0 to finish): "))
            if item_id == 0:
                break
            item = restaurant.find_menu_item(item_id)
            if item is None:
                print("Menu item not found.")
                continue
            quantity = int(input("Quantity: "))
            builder.add_item(item, quantity)

        order = builder.build()
        restaurant.create_order(order)
        print("\nOrder created successfully.")
        print(order)
    except Exception as error:
        print("Error:", error)

def close_order_ui(restaurant: Restaurant):
    try:
        order_id = int(input("Enter order ID to close: "))
        restaurant.close_order(order_id)
    except Exception as error:
        print("Error:", error)

def reserve_table_ui(restaurant: Restaurant):
    try:
        table_number = int(input("Enter table number to reserve: "))
        restaurant.reserve_table_manually(table_number)
        print("Table reserved successfully.")
    except Exception as error:
        print("Error:", error)

def free_table_ui(restaurant: Restaurant):
    try:
        table_number = int(input("Enter table number to free: "))
        restaurant.free_table_manually(table_number)
        print("Table freed successfully.")
    except Exception as error:
        print("Error:", error)

def main():
    restaurant = Restaurant("Restaurant Management System")
    load_default_data(restaurant)

    while True:
        print("\n=== RESTAURANT MANAGEMENT SYSTEM ===")
        print("1. Show menu")
        print("2. Add menu item")
        print("3. Remove menu item")
        print("4. Show tables")
        print("5. Reserve table")
        print("6. Free table")
        print("7. Create order")
        print("8. Show orders")
        print("9. Close order")
        print("10. Show total revenue")
        print("11. Save data and Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            restaurant.show_menu()
        elif choice == "2":
            add_menu_item_ui(restaurant)
        elif choice == "3":
            remove_menu_item_ui(restaurant)
        elif choice == "4":
            restaurant.show_tables()
        elif choice == "5":
            reserve_table_ui(restaurant)
        elif choice == "6":
            free_table_ui(restaurant)
        elif choice == "7":
            create_order_ui(restaurant)
        elif choice == "8":
            restaurant.show_orders()
        elif choice == "9":
            close_order_ui(restaurant)
        elif choice == "10":
            print(f"Total revenue: {restaurant.total_revenue():.2f} EUR")
        elif choice == "11":
            restaurant.save_orders("restaurant_data.json")
            print("Program finished successfully.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()


