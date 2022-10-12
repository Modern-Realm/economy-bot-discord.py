from bank_funcs import DB

import discord
import mysql.connector as mysql

from typing import Union, Any, Optional

__all__ = [
    "shop_items",
    "open_inv",
    "get_inv_data",
    "update_inv",
    "change_inv"
]

table_name = "inventory"  # Enter the table name here (tip:- use only lowercase letters)

shop_items = [
    {"name": "watch", "cost": 100, "id": 1, "info": "It's a watch"},
    {"name": "mobile", "cost": 1000, "id": 2, "info": "It's a mobile"},
    {"name": "laptop", "cost": 10000, "id": 3, "info": "It's a laptop"}
    # You can add your items here ...
]


async def create_table() -> None:
    db = DB()
    cols = [item["name"] for item in shop_items]

    db.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}`(userID BIGINT)")
    for col in cols:
        try:
            db.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` INTEGER")
        except mysql.errors.ProgrammingError:
            pass


async def open_inv(user: discord.Member) -> None:
    await create_table()

    db = DB()
    data = db.execute(f"SELECT * FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")

    if data is None:
        db.execute(f"INSERT INTO `{table_name}`(userID) VALUES(%s)", (user.id,))

        for item in shop_items:
            item_name = item["name"]
            db.execute(f"UPDATE `{table_name}` SET `{item_name}` = 0 WHERE userID = %s", (user.id,))


async def get_inv_data(user: discord.Member) -> Optional[Any]:
    users = DB().execute(f"SELECT * FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")
    return users


async def update_inv(user: discord.Member, amount: Union[float, int], mode: str) -> Optional[Any]:
    db = DB()
    data = db.execute(f"SELECT * FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")

    if data is not None:
        db.execute(f"UPDATE `{table_name}` SET `{mode}` = `{mode}` + %s WHERE userID = %s", (amount, user.id))

    users = db.execute(f"SELECT `{mode}` FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")
    return users


async def change_inv(user: discord.Member, amount: Union[float, int, None], mode: str) -> Optional[Any]:
    db = DB()
    data = db.execute(f"SELECT * FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")

    if data is not None:
        db.execute(f"UPDATE `{table_name}` SET `{mode}` = %s WHERE userID = %s", (amount, user.id))

    users = db.execute(f"SELECT `{mode}` FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")
    return users
