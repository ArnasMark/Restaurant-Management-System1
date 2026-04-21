class MenuItem(ABC):
    def __init__(self, item_id: int, name: str, price: float):
        if item_id <= 0:
            raise ValueError("Item ID must be positive.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
