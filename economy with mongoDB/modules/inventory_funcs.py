from modules.bank_funcs import DB

import discord

from pymongo import errors
from typing import Union, Any, Optional

__all__ = [
    "shop_items",
    "open_inv",
    "get_inv_data",
    "update_inv",
    "change_inv"
]

TABLE_NAME = "inventory"  # Enter the table name here (tip:- use only lowercase letters)

shop_items = [
    {"name": "watch", "cost": 100, "id": 1, "info": "It's a watch"},
    {"name": "mobile", "cost": 1000, "id": 2, "info": "It's a mobile"},
    {"name": "laptop", "cost": 10000, "id": 3, "info": "It's a laptop"}
    # You can add your items here ...
]
item_names = [item["name"] for item in shop_items]


async def create_table():
    if TABLE_NAME not in DB.db.list_collection_names():
        DB.db.create_collection(TABLE_NAME)


async def open_inv(user: discord.Member):
    doc = {"_id": user.id}
    user_data = DB.cursor(TABLE_NAME).find_one(doc)
    if user_data is not None:
        return

    for name in item_names:
        doc.setdefault(name, 0)
    DB.cursor(TABLE_NAME).insert_one(doc)


async def get_inv_data(user: discord.Member, mode: str = None) -> Optional[Any]:
    user_data = DB.cursor(TABLE_NAME).find_one({"_id": user.id})
    if mode is None:
        return [_ for _ in user_data.values()]

    return user_data.get(mode)


async def update_inv(user: discord.Member, amount: Union[float, int], mode: str) -> Optional[Any]:
    DB.cursor(TABLE_NAME).update_one(
        {"_id": user.id}, {"$inc": {mode: amount}}
    )

    return await get_inv_data(user, mode)


async def change_inv(user: discord.Member, amount: Union[float, int, None], mode: str) -> Optional[Any]:
    DB.cursor(TABLE_NAME).update_one(
        {"_id": user.id}, {"$set": {mode: amount}}
    )

    return await get_inv_data(user, mode)
