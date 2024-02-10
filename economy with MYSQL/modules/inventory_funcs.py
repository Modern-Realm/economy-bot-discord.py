from modules.ext import Database

import discord
import mysql.connector as mysql

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
        self.db = database

    @property
    def shop_items(self) -> List:
        return shop_items

    async def create_table(self) -> None:
        conn = await self.db.connect()
        await self.db.run(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)", conn=conn)
        for col in item_names:
            try:
                await self.db.run(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` INTEGER DEFAULT 0", conn=conn)
            except mysql.errors.ProgrammingError:
                pass

        conn.close()

    async def open_acc(self, user: discord.Member) -> None:
        conn = await self.db.connect()
        data = await self.db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s",
            (user.id,), fetch="one", conn=conn
        )

        if data is None:
            await self.db.run(
                f"INSERT INTO `{TABLE_NAME}`(userID) VALUES(%s)",
                (user.id,), conn=conn
            )

            for item in item_names:
                await self.db.run(
                    f"UPDATE `{TABLE_NAME}` SET `{item}` = 0 WHERE userID = %s",
                    (user.id,), conn=conn
                )

            conn.close()

    async def get_acc(self, user: discord.Member) -> Optional[Any]:
        return await self.db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,),
            fetch="one"
        )

    async def update_acc(self, user: discord.Member, amount: int, mode: str) -> Optional[Any]:
        conn = await self.db.connect()
        data = await self.db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s",
            (user.id,), fetch="one", conn=conn
        )

        if data is not None:
            await self.db.run(
                f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + %s WHERE userID = %s",
                (amount, user.id), conn=conn
            )

        users = await self.db.execute(
            f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = %s",
            (user.id,), fetch="one", conn=conn
        )

        conn.close()
        return users

    async def change_acc(self, user: discord.Member, amount: Union[int, None], mode: str) -> Optional[Any]:
        conn = await self.db.connect()
        data = await self.db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s",
            (user.id,), fetch="one", conn=conn
        )

        if data is not None:
            await self.db.run(
                f"UPDATE `{TABLE_NAME}` SET `{mode}` = %s WHERE userID = %s",
                (amount, user.id), conn=conn
            )

        users = await self.db.execute(
            f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = %s",
            (user.id,), fetch="one", conn=conn
        )
        conn.close()
        return users
