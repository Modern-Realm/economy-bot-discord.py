from modules.ext import Database

import discord

from typing import Mapping, Any, Optional, Union, List
from pymongo import MongoClient, errors
from pymongo.database import Database as MongoDB
from pymongo.collection import Collection

__all__ = [
    "Bank"
]

TABLE_NAME = "bank"

# You can add as many columns as you can in this list !!!
document = {
    "_id": None,
    "wallet": 5000,
    "bank": 0
}
cols = [key for key in document.keys()]


class Bank:
    def __init__(self, database: Database):
        self._conn = database

    async def create_table(self):
        if TABLE_NAME not in self._conn.db.list_collection_names():
            self._conn.db.create_collection(TABLE_NAME)

    async def open_acc(self, user: discord.Member) -> None:
        user_data = self._conn.cursor(TABLE_NAME).find_one({"_id": user.id})
        if user_data is not None:
            return

        doc = document.copy()
        doc.update(_id=user.id)
        self._conn.cursor(TABLE_NAME).insert_one(doc)

    async def get_acc(self, user: discord.Member, mode: str = None) -> Optional[Any]:
        user_data = self._conn.cursor(TABLE_NAME).find_one({"_id": user.id})
        if mode is None:
            return [_ for _ in user_data.values()]

        return user_data.get(mode)

    async def update_acc(
        self, user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet"
    ) -> Optional[Any]:
        self._conn.cursor(TABLE_NAME).update_one(
            {"_id": user.id}, {"$inc": {mode: amount}}
        )

        return await self.get_acc(user, mode)

    async def reset_acc(self, user: discord.Member) -> None:
        self._conn.cursor(TABLE_NAME).delete_one({"_id": user.id})
        await self.open_acc(user)

    async def get_networth_lb(self) -> List[Any]:
        user_data = self._conn.cursor(TABLE_NAME).aggregate([
            {"$addFields": {"sum": {"$add": ["$wallet", "$bank"]}}},
            {"$sort": {"sum": -1}}
        ])
        # sorted_data = []
        # for val in user_data:
        #     sorted_data.append([_ for _ in val.values()])

        return [[_ for _ in val.values()] for val in user_data]
