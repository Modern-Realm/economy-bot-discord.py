import mysql.connector as mysql
import discord

from typing import Any, Optional

from modules.ext import Database

__all__ = [
    "Bank"
]

TABLE_NAME = "bank"
columns = ["wallet", "bank"]  # You can add more Columns in it !


class Bank:
    def __init__(self, database: Database):
        self.db = database

    async def create_table(self) -> None:
        conn = await self.db.connect()
        await self.db.run(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)", conn=conn)
        for col in columns:
            try:
                await self.db.run(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` BIGINT DEFAULT 0", conn=conn)
            except mysql.errors.ProgrammingError:
                pass

        conn.close()

    async def open_acc(self, user: discord.Member) -> None:
        conn = await self.db.connect()
        data = await self.db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,), fetch="one", conn=conn
        )
        if data is None:
            await self.db.run(
                f"INSERT INTO `{TABLE_NAME}`(userID, wallet) VALUES(%s, %s)", \
                (user.id, 5000), conn=conn
            )

        conn.close()

    async def get_acc(self, user: discord.Member) -> Optional[Any]:
        return await self.db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,), fetch="one"
        )

    async def update_acc(
        self, user: discord.Member, amount: int = 0, mode: str = "wallet"
    ) -> Optional[Any]:
        conn = await self.db.connect()
        data = await self.db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,), fetch="one",
            conn=conn
        )
        if data is not None:
            await self.db.run(
                f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + %s WHERE userID = %s",
                (amount, user.id), conn=conn
            )

        users = await self.db.execute(
            f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,),
            fetch="one", conn=conn
        )

        conn.close()
        return users

    async def reset_acc(self, user: discord.Member) -> None:
        await self.db.run(f"DELETE FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,))
        await self.open_acc(user)

    async def get_networth_lb(self) -> Any:
        return await self.db.execute(
            f"SELECT `userID`, `wallet` + `bank` FROM `{TABLE_NAME}` ORDER BY `wallet` + `bank` DESC",
            fetch="all")
