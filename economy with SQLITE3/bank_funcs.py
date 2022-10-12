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

filename = ...  # Enter your file_name here , with (.db, .sql, .sqlite3) suffix , Example: economy.db
table_name = ...  # Enter the table name here (tip:- use only lowercase letters)


class Database:
    @staticmethod
    def _connect():
        return sqlite3.connect(filename)

    @staticmethod
    def _fetch(cursor, mode) -> Optional[Any]:
        if mode == "one":
            return cursor.fetchone()
        if mode == "many":
            return cursor.fetchmany()
        if mode == "all":
            return cursor.fetchall()

        return None

    def execute(self, query: str, values: Tuple = (), *, fetch: str = None) -> Optional[Any]:
        db = self._connect()
        cursor = db.cursor()

        cursor.execute(query, values)
        data = self._fetch(cursor, fetch)
        db.commit()

        cursor.close()
        db.close()

        return data


DB = Database


async def create_table() -> None:
    db = DB()
    cols = ["wallet", "bank"]  # You can add as many as columns in this !!!

    db.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}`(userID BIGINT)")
    for col in cols:
        try:
            db.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` BIGINT")
        except sqlite3.OperationalError:
            pass


async def open_bank(user: discord.Member) -> None:
    await create_table()
    columns = ["wallet", "bank"]  # You can add more Columns in it !

    db = DB()
    data = db.execute(f"SELECT * FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")

    if data is None:
        db.execute(f"INSERT INTO `{table_name}`(userID) VALUES(?)", (user.id,))

        for name in columns:
            db.execute(f"UPDATE `{table_name}` SET `{name}` = ? WHERE userID = ?", (0, user.id))

        db.execute(f"UPDATE `{table_name}` SET `wallet` = ? WHERE userID = ?", (5000, user.id))


async def get_bank_data(user: discord.Member) -> Optional[Any]:
    users = DB().execute(f"SELECT * FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet") -> Optional[Any]:
    db = DB()
    data = db.execute(
        f"SELECT * FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")
    if data is not None:
        db.execute(f"UPDATE `{table_name}` SET `{mode}` = `{mode}` + ? WHERE userID = ?", (amount, user.id))

    users = db.execute(f"SELECT `{mode}` FROM `{table_name}` WHERE userID = ?", (user.id,), fetch="one")
    return users


async def get_networth_lb() -> Any:
    users = DB().execute(f"SELECT `userID`, `wallet` + `bank` FROM `{table_name}` ORDER BY `wallet` + `bank` DESC",
                         fetch="all")
    return users
