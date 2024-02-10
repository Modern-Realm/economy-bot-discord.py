from modules.ext import Database

import aiosqlite
import discord

from typing import Union, List, Any, Optional

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
        self._db = database

    @property
    def shop_items(self) -> List:
        return shop_items

    async def create_table(self) -> None:
        conn = await self._db.connect()
        await self._db.run(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)", conn=conn)
        for col in item_names:
            try:
                await self._db.run(
                    f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` INTEGER DEFAULT 0",
                    conn=conn
                )
            except aiosqlite.OperationalError:
                pass

        await conn.close()

    async def open_acc(self, user: discord.Member) -> None:
        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?",
            (user.id,), fetch="one", conn=conn
        )
        if data is None:
            await self._db.run(
                f"INSERT INTO `{TABLE_NAME}`(userID) VALUES(?)",
                (user.id,), conn=conn
            )

        await conn.close()

    async def get_acc(self, user: discord.Member) -> Optional[Any]:
        users = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?",
            (user.id,), fetch="one"
        )
        return users

    async def update_acc(
        self, user: discord.Member, amount: int, mode: str
    ) -> Optional[Any]:
        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?",
            (user.id,), fetch="one", conn=conn
        )
        if data is not None:
            await self._db.run(
                f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + ? WHERE userID = ?",
                (amount, user.id), conn=conn
            )

        users = await self._db.execute(
            f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ?",
            (user.id,), fetch="one", conn=conn
        )

        await conn.close()
        return users

    async def change_acc(self, user: discord.Member, amount: Union[int, None], mode: str) -> Optional[Any]:
        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?",
            (user.id,), fetch="one", conn=conn)
        if data is not None:
            await self._db.run(
                f"UPDATE `{TABLE_NAME}` SET `{mode}` = ? WHERE userID = ?",
                (amount, user.id), conn=conn
            )

        users = await self._db.execute(
            f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ?",
            (user.id,), fetch="one", conn=conn
        )

        await conn.close()
        return users
