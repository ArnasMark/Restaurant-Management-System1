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
