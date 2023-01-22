from config import Auth

import mysql.connector as mysql
import discord

from mysql.connector import MySQLConnection, errors
from typing import Tuple, Any, Optional, Union

__all__ = [
    "DB",
    "open_bank",
    "get_bank_data",
    "update_bank",
    "get_networth_lb"
]

TABLE_NAME = "bank"
columns = ["wallet", "bank"]  # You can add more Columns in it !


class Database:
    def __init__(self):
        self.conn: Optional[MySQLConnection] = None

    async def connect(self):
        try:
            self.conn = mysql.connect(
                host=Auth.DB_HOST, port=Auth.DB_PORT,
                database=Auth.DB_NAME, user=Auth.DB_USER, passwd=Auth.DB_PASSWD,
            )
        except errors.Error:
            self.conn = None
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
        except mysql.errors.ProgrammingError:
            pass


async def open_bank(user: discord.Member) -> None:
    data = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,), fetch="one")
    if data is None:
        await DB.execute(f"INSERT INTO `{TABLE_NAME}`(userID) VALUES(%s)", (user.id,))

        for name in columns:
            await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{name}` = %s WHERE userID = %s", (0, user.id))

        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `wallet` = %s WHERE userID = %s", (5000, user.id))


async def get_bank_data(user: discord.Member) -> Optional[Any]:
    return await DB.execute(
        f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,),
        fetch="one")


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet") -> Optional[Any]:
    data = await DB.execute(f"SELECT * FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,), fetch="one")
    if data is not None:
        await DB.execute(f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{mode}` + %s WHERE userID = %s",
                         (amount, user.id))

    users = await DB.execute(f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = %s", (user.id,), fetch="one")
    return users


async def get_networth_lb() -> Any:
    return await DB.execute(
        f"SELECT `userID`, `wallet` + `bank` FROM `{TABLE_NAME}` ORDER BY `wallet` + `bank` DESC",
        fetch="all")
