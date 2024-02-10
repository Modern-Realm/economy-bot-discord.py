from .ext import Database as DB
from .bank_funcs import Bank
from .inventory_funcs import Inventory

__all__ = [
    "Database"
]


class Database(DB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bank = Bank(self)
        self.inv = Inventory(self)
