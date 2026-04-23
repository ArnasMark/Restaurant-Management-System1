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
