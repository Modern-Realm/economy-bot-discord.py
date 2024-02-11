from modules.ext import Database

import discord

from typing import List, Union, Any, Optional

__all__ = [
    "Inventory"
]

TABLE_NAME = "inventory"  # Enter the table name here (tip:- use only lowercase letters)

shop_items = [
    {"name": "watch", "cost": 100, "id": 1, "info": "It's a watch"},
    {"name": "mobile", "cost": 1000, "id": 2, "info": "It's a mobile"},
    {"name": "laptop", "cost": 10000, "id": 3, "info": "It's a laptop"}
    # You can add your items here ...
]
item_names = [item["name"] for item in shop_items]


class Inventory:
    def __init__(self, database: Database):
        self._conn = database

    @property
    def shop_items(self) -> List:
        return shop_items

    async def create_table(self):
        if TABLE_NAME not in self._conn.db.list_collection_names():
            self._conn.db.create_collection(TABLE_NAME)

    async def open_acc(self, user: discord.Member):
        doc = {"_id": user.id}
        user_data = self._conn.cursor(TABLE_NAME).find_one(doc)
        if user_data is not None:
            return

        for name in item_names:
            doc.setdefault(name, 0)
        self._conn.cursor(TABLE_NAME).insert_one(doc)

    async def get_acc(self, user: discord.Member, mode: str = None) -> Optional[Any]:
        user_data = self._conn.cursor(TABLE_NAME).find_one({"_id": user.id})
        if mode is None:
            return [_ for _ in user_data.values()]

        return user_data.get(mode)

    async def update_acc(
        self, user: discord.Member, amount: Union[float, int], mode: str
    ) -> Optional[Any]:
        self._conn.cursor(TABLE_NAME).update_one(
            {"_id": user.id}, {"$inc": {mode: amount}}
        )

        return [await self.get_acc(user, mode)]

    async def change_acc(
        self, user: discord.Member, amount: Union[float, int, None], mode: str
    ) -> Optional[Any]:
        self._conn.cursor(TABLE_NAME).update_one(
            {"_id": user.id}, {"$set": {mode: amount}}
        )

        return await self.get_acc(user, mode)
