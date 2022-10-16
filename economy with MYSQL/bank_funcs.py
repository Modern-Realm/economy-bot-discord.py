import mysql.connector as mysql
import discord

from typing import Tuple, Any, Optional, Union

__all__ = [
    "DB",
    "open_bank",
    "get_bank_data",
    "update_bank",
    "get_networth_lb"
]

DB_HOST = "localhost"  # or your selected port/id address
DB_USER = ...  # enter the username you created or root user
DB_PASSWD = ...  # enter the password you have given for user or root user
DB_NAME = ...  # enter the database name which you created !

table_name = ...  # Enter the table name here (tip:- use only lowercase letters)


class Database:
    @staticmethod
    def _connect():
        return mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)

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
        except mysql.errors.ProgrammingError:
            pass


async def open_bank(user: discord.Member) -> None:
    await create_table()
    columns = ["wallet", "bank"]  # You can add more Columns in it !

    db = DB()
    data = db.execute(f"SELECT * FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")

    if data is None:
        db.execute(f"INSERT INTO `{table_name}`(userID) VALUES(%s)", (user.id,))

        for name in columns:
            db.execute(f"UPDATE `{table_name}` SET `{name}` = %s WHERE userID = %s", (0, user.id))

        db.execute(f"UPDATE `{table_name}` SET `wallet` = %s WHERE userID = %s", (5000, user.id))


async def get_bank_data(user: discord.Member) -> Optional[Any]:
    users = DB().execute(f"SELECT * FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")
    return users


async def update_bank(user: discord.Member, amount: Union[float, int] = 0, mode: str = "wallet") -> Optional[Any]:
    db = DB()
    data = db.execute(f"SELECT * FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")
    if data is not None:
        db.execute(f"UPDATE `{table_name}` SET `{mode}` = `{mode}` + %s WHERE userID = %s",
                   (amount, user.id))

    users = db.execute(f"SELECT `{mode}` FROM `{table_name}` WHERE userID = %s", (user.id,), fetch="one")
    return users


async def get_networth_lb() -> Any:
    users = DB().execute(f"SELECT `userID`, `wallet` + `bank` FROM `{table_name}` ORDER BY `wallet` + `bank` DESC",
                         fetch="all")
    return users
