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

table_name = "bank"  # Enter the table name here (tip:- use only lowercase letters)


class Database:
    @staticmethod
    async def _connect():
        return await aiosqlite.connect(Auth.filename)

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
        db = await self._connect()
        cursor = await db.cursor()

        await cursor.execute(query, values)
        data = await self._fetch(cursor, fetch)
        await db.commit()

        await cursor.close()
        await db.close()

        return data


DB = Database


async def create_table() -> None:
    db = DB()
    cols = ["wallet", "bank"]  # You can add as many as columns in this !!!

    await db.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}`(userID BIGINT)")
    for col in cols:
        try:
            await db.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` BIGINT")
        except aiosqlite.OperationalError:
            pass


async def open_bank(user: discord.Member) -> None:
    await create_table()
    columns = ["wallet", "bank"]  # You can add more Columns in it !

    db = DB()
    data = await db.execute(f"SELECT * FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")

    if data is None:
        await db.execute(f"INSERT INTO `{table_name}`(userID) VALUES(?)", (user.id,))

        for name in columns:
            await db.execute(f"UPDATE `{table_name}` SET `{name}` = ? WHERE userID = ?", (0, user.id))

        await db.execute(f"UPDATE `{table_name}` SET `wallet` = ? WHERE userID = ?", (5000, user.id))


async def get_bank_data(user: discord.Member) -> Optional[Any]:
    users = await DB().execute(f"SELECT * FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet") -> Optional[Any]:
    db = DB()
    data = await db.execute(
        f"SELECT * FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")
    if data is not None:
        await db.execute(f"UPDATE `{table_name}` SET `{mode}` = `{mode}` + ? WHERE userID = ?", (amount, user.id))

    users = await db.execute(f"SELECT `{mode}` FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def get_networth_lb() -> Any:
    users = await DB().execute(
        f"SELECT `userID`, `wallet` + `bank` FROM `{table_name}` ORDER BY `wallet` + `bank` DESC", fetch="all")
    return users
