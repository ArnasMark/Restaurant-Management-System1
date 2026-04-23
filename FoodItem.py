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
