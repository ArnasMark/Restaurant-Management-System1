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
