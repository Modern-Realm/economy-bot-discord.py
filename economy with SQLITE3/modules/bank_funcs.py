from modules.ext import Database

import sqlite3
import discord

from typing import Any, Optional

__all__ = [
    "Bank"
]

TABLE_NAME = "economy"
columns = ["wallet", "bank"]  # You can add more Columns in it !


class Bank:
    def __init__(self, database: Database):
        self._db = database

    async def create_table(self) -> None:
        conn = await self._db.connect()
        await self._db.run(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)", conn=conn)
        for col in columns:
            try:
                await self._db.run(
                    f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` BIGINT DEFAULT 0", conn=conn
                )
            except sqlite3.OperationalError:
                pass

        conn.close()

    async def open_acc(self, user: discord.Member) -> None:
        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,),
            fetch="one", conn=conn
        )

        if data is None:
            await self._db.run(
                f"INSERT INTO `{TABLE_NAME}`(userID, wallet) VALUES(?, ?)",
                (user.id, 5000), conn=conn
            )

        conn.close()

    async def get_acc(self, user: discord.Member) -> Optional[Any]:
        users = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one"
        )
        return users

    async def update_acc(
        self, user: discord.Member, amount: int = 0, mode: str = "wallet"
    ) -> Optional[Any]:
        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,),
            fetch="one", conn=conn
        )
        if data is not None:
            await self._db.run(
                f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + ? WHERE userID = ?",
                (amount, user.id), conn=conn
            )

        users = await self._db.execute(
            f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,),
            fetch="one", conn=conn
        )

        conn.close()
        return users

    async def reset_acc(self, user: discord.Member) -> None:
        await self._db.run(f"DELETE FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,))
        await self.open_acc(user)

    async def get_networth_lb(self) -> Any:
        users = await self._db.execute(
            f"SELECT `userID`, `wallet` + `bank` FROM `{TABLE_NAME}` ORDER BY `wallet` + `bank` DESC",
            fetch="all"
        )
        return users
