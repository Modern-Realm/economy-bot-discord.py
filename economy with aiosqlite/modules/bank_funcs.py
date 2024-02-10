from modules.ext import Database

import aiosqlite
import discord

from typing import Any, Optional

__all__ = [
    "Bank"
]

TABLE_NAME = "bank"  # Enter the table name here (tip:- use only lowercase letters)
columns = ["wallet", "bank"]  # You can add more Columns in it !


class Bank:
    def __init__(self, database: Database):
        self._db = database

    async def create_table(self) -> None:
        conn = await self._db.connect()
        await self._db.run(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)", conn=conn)
        for col in columns:
            try:
                await self._db.run(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` BIGINT DEFAULT 0", conn=conn)
            except aiosqlite.OperationalError:
                pass

        await conn.close()

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

        await conn.close()

    async def get_acc(self, user: discord.Member) -> Optional[Any]:
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?",
            (user.id,), fetch="one"
        )

    async def update_acc(
        self, user: discord.Member, amount: int = 0, mode: str = "wallet"
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

    async def reset_acc(self, user: discord.Member) -> None:
        await self._db.execute(f"DELETE FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,))
        await self.open_acc(user)

    async def get_networth_lb(self) -> Any:
        return await self._db.execute(
            f"SELECT `userID`, `wallet` + `bank` FROM `{TABLE_NAME}` ORDER BY `wallet` + `bank` DESC",
            fetch="all"
        )
