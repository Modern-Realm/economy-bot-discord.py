import sqlite3

from typing import Optional, Any, Tuple


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

    @staticmethod
    async def _fetch(cursor: sqlite3.Cursor, mode: str) -> Optional[Any]:
        if mode == "one":
            return cursor.fetchone()
        if mode == "many":
            return cursor.fetchmany()
        if mode == "all":
            return cursor.fetchall()

        return None

    async def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    async def execute(
        self, query: str, values: Tuple = (), *, fetch: str = None, commit: bool = False,
        conn: sqlite3.Connection = None
    ) -> Optional[Any]:
        bypass = conn
        conn = await self.connect() if conn is None else conn
        cursor = conn.cursor()

        cursor.execute(query, values)
        if fetch is not None:
            data = await self._fetch(cursor, fetch)
        else:
            data = None

        if commit:
            conn.commit()

        cursor.close()
        if bypass is None:
            conn.close()

        return data

    async def run(self, query: str, values: Tuple = (), *, conn: sqlite3.Connection = None) -> None:
        await self.execute(query, values, commit=True, conn=conn)
