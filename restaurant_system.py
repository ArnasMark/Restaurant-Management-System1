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
