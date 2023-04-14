from modules.bank_funcs import DB

import aiosqlite
import discord

from typing import Union, Any, Optional

__all__ = [
    "DB",
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


async def create_table() -> None:
    await DB.execute(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)")
    for col in item_names:
        try:
            await DB.execute(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` INTEGER DEFAULT 0")
        except aiosqlite.OperationalError:
            pass


async def open_inv(user: discord.Member) -> None:
    data = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    if data is None:
        await DB.execute(f"INSERT INTO `{TABLE_NAME}`(userID) VALUES(?)", (user.id,))

        for item in shop_items:
            item_name = item["name"]
            await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{item_name}` = ? WHERE userID = ?", (0, user.id,))


async def get_inv_data(user: discord.Member) -> Optional[Any]:
    users = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def update_inv(user: discord.Member, amount: Union[float, int], mode: str) -> Optional[Any]:
    data = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    if data is not None:
        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + ? WHERE userID = ?", (amount, user.id))

    users = await DB.execute(f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def change_inv(user: discord.Member, amount: Union[float, int, None], mode: str) -> Optional[Any]:
    data = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    if data is not None:
        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{mode}` = ? WHERE userID = ?", (amount, user.id))

    users = await DB.execute(f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    return users
