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


