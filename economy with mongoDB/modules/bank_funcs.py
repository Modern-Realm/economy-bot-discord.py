from config import Auth

import discord

from typing import Any, Optional, Tuple, Union, Mapping
from pymongo import MongoClient
from pymongo.database import Database

__all__ = [
    "DB",
    "open_bank",
    "get_bank_data",
    "update_bank",
    "get_networth_lb"
]

table_name = "bank"


def database() -> Database[Mapping[str, Any]]:
    return MongoClient(Auth.AUTH_URL)[Auth.DB_NAME]


DB = database


async def open_bank(user: discord.Member) -> None:
    columns = ["wallet", "bank"]  # You can add more Columns in it !
    cursor = DB()[table_name]

    data = cursor.find_one({"_id": user.id})
    if data is None:
        cursor.insert_one({"_id": user.id})
        for col in columns:
            try:
                cursor.update_one({"_id": user.id}, {"$set": {col: 0}})
            except:
                pass
        cursor.update_one({"_id": user.id}, {"$set": {"wallet": 5000}})


async def get_bank_data(user: discord.Member) -> Optional[Any]:
    cursor = DB()[table_name]
    data = cursor.find_one({"_id": user.id}, max_time_ms=100)
    if data is None:
        return None

    return [val for val in data.values()]


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet"):
    cursor = DB()[table_name]
    cursor.update_one({"_id": user.id}, {"$inc": {mode: amount}})


async def get_networth_lb() -> Any:
    cursor = DB()[table_name]
    data = cursor.find({}, max_time_ms=100).sort([("wallet", -1), ("bank", -1)])

    raw = []
    for doc in data:
        raw.append([val for val in doc.values()])

    return raw
