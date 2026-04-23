class OrderItem:
    def __init__(self, menu_item: MenuItem, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.menu_item = menu_item
        self.quantity = quantity

    def subtotal(self) -> float:
        return self.menu_item.final_price() * self.quantity
