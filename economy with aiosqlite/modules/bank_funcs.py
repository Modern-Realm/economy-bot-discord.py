from config import Auth

import aiosqlite
import discord

from typing import Tuple, Any, Optional, Union

__all__ = [
    "DB",
    "open_bank",
    "get_bank_data",
    "update_bank",
    "get_networth_lb"
]

TABLE_NAME = "bank"  # Enter the table name here (tip:- use only lowercase letters)
columns = ["wallet", "bank"]  # You can add more Columns in it !


class Database:
    def __init__(self):
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        try:
            self.conn = await aiosqlite.connect(Auth.FILENAME)
        except aiosqlite.Error:
            pass

    @property
    def is_connected(self) -> bool:
        return self.conn is not None

    @staticmethod
    async def _fetch(cursor, mode) -> Optional[Any]:
        if mode == "one":
            return await cursor.fetchone()
        if mode == "many":
            return await cursor.fetchmany()
        if mode == "all":
            return await cursor.fetchall()

        return None

    async def execute(self, query: str, values: Tuple = (), *, fetch: str = None) -> Optional[Any]:
        cursor = await self.conn.cursor()

        await cursor.execute(query, values)
        data = await self._fetch(cursor, fetch)
        await self.conn.commit()

        await cursor.close()
        return data


DB = Database()


async def create_table() -> None:
    await DB.execute(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)")
    for col in columns:
        try:
            await DB.execute(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` BIGINT")
        except aiosqlite.OperationalError:
            pass


async def open_bank(user: discord.Member) -> None:
    data = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    if data is None:
        await DB.execute(f"INSERT INTO `{TABLE_NAME}`(userID) VALUES(?)", (user.id,))

        for name in columns:
            await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{name}` = ? WHERE userID = ?", (0, user.id))

        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `wallet` = ? WHERE userID = ?", (5000, user.id))


async def get_bank_data(user: discord.Member) -> Optional[Any]:
    return await DB.execute(
        f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,),
        fetch="one")


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet") -> Optional[Any]:
    data = await DB.execute(
        f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    if data is not None:
        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + ? WHERE userID = ?", (amount, user.id))

    users = await DB.execute(f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def get_networth_lb() -> Any:
    return await DB.execute(
        f"SELECT `userID`, `wallet` + `bank` FROM `{TABLE_NAME}` ORDER BY `wallet` + `bank` DESC",
        fetch="all")
