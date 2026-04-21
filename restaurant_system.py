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
