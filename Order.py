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
