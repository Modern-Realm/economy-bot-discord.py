from config import Auth

import discord

from typing import Mapping, Any, Optional, Union, List
from pymongo import MongoClient, errors
from pymongo.database import Database as MongoDB
from pymongo.collection import Collection

__all__ = [
    "DB",
    "open_bank",
    "get_bank_data",
    "update_bank",
    "get_networth_lb"
]

TABLE_NAME = "bank"

# You can add as many columns as you can in this list !!!
document = {
    "_id": None,
    "wallet": 5000,
    "bank": 0
}
cols = [key for key in document.keys()]


class DataBase:
    def __init__(self):
        self.cluster: Optional[MongoClient[Mapping[str, Any]]] = None
        self.db: Optional[MongoDB[Mapping[str, Any]]] = None

    async def connect(self):
        try:
            self.cluster = MongoClient(Auth.CLUSTER_AUTH_URL)
            self.db = self.cluster[Auth.DB_NAME]
        except errors.OperationFailure:
            self.cluster = None
        return self

    @property
    def is_connected(self) -> bool:
        return False if self.cluster is None else True

    def cursor(self, table_name: str) -> Collection[Mapping[str, Any]]:
        return self.db[table_name]


DB = DataBase()


async def create_table():
    if TABLE_NAME not in DB.db.list_collection_names():
        DB.db.create_collection(TABLE_NAME)


async def open_bank(user: discord.Member) -> None:
    user_data = DB.cursor(TABLE_NAME).find_one({"_id": user.id})
    if user_data is not None:
        return

    doc = document.copy()
    doc.update(_id=user.id)
    DB.cursor(TABLE_NAME).insert_one(doc)


async def get_bank_data(user: discord.Member, mode: str = None) -> Optional[Any]:
    user_data = DB.cursor(TABLE_NAME).find_one({"_id": user.id})
    if mode is None:
        return [_ for _ in user_data.values()]

    return user_data.get(mode)


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet") -> Optional[Any]:
    DB.cursor(TABLE_NAME).update_one(
        {"_id": user.id}, {"$inc": {mode: amount}}
    )

    return await get_bank_data(user, mode)


async def get_networth_lb() -> List[Any]:
    user_data = DB.cursor(TABLE_NAME).aggregate([
        {"$addFields": {"sum": {"$add": ["$wallet", "$bank"]}}},
        {"$sort": {"sum": -1}}
    ])
    sorted_data = []
    for val in user_data:
        sorted_data.append([_ for _ in val.values()])

    return sorted_data
