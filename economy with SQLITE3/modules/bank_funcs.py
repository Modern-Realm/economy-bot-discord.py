from config import Auth

import sqlite3
import discord

from typing import Tuple, Any, Optional, Union

__all__ = [
    "DB",
    "open_bank",
    "get_bank_data",
    "update_bank",
    "get_networth_lb"
]

TABLE_NAME = "economy"
columns = ["wallet", "bank"]  # You can add more Columns in it !


class Database:
    def __init__(self):
        self.conn: Optional[sqlite3.Connection] = None

    async def connect(self):
        try:
            self.conn = sqlite3.connect(Auth.FILENAME)
        except sqlite3.Error:
            pass

        return self

    @property
    def is_connected(self) -> bool:
        return False if self.conn is None else True

    @staticmethod
    async def _fetch(cursor, mode) -> Optional[Any]:
        if mode == "one":
            return cursor.fetchone()
        if mode == "many":
            return cursor.fetchmany()
        if mode == "all":
            return cursor.fetchall()

        return None

    async def execute(self, query: str, values: Tuple = (), *, fetch: str = None) -> Optional[Any]:
        cursor = self.conn.cursor()

        cursor.execute(query, values)
        data = await self._fetch(cursor, fetch)
        self.conn.commit()

        cursor.close()
        return data


DB = Database()


async def create_table() -> None:
    await DB.execute(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(userID BIGINT)")
    for col in columns:
        try:
            await DB.execute(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` BIGINT")
        except sqlite3.OperationalError:
            pass


async def open_bank(user: discord.Member) -> None:
    data = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")

    if data is None:
        await DB.execute(f"INSERT INTO `{TABLE_NAME}`(userID) VALUES(?)", (user.id,))

        for name in columns:
            await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{name}` = ? WHERE userID = ?", (0, user.id))

        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `wallet` = ? WHERE userID = ?", (5000, user.id))


async def get_bank_data(user: discord.Member) -> Optional[Any]:
    users = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet") -> Optional[Any]:
    data = await DB.execute(
        f"SELECT * FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    if data is not None:
        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + ? WHERE userID = ?", (amount, user.id))

    users = await DB.execute(f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def get_networth_lb() -> Any:
    users = await DB.execute(f"SELECT `userID`, `wallet` + `bank` FROM `{TABLE_NAME}` ORDER BY `wallet` + `bank` DESC",
                             fetch="all")
    return users
