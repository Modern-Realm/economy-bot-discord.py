import aiosqlite

from typing import Optional, Any, Tuple


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

    @staticmethod
    async def _fetch(cursor: aiosqlite.Cursor, mode: str) -> Optional[Any]:
        if mode == "one":
            return await cursor.fetchone()
        if mode == "many":
            return await cursor.fetchmany()
        if mode == "all":
            return await cursor.fetchall()

        return None

    async def connect(self) -> aiosqlite.Connection:
        return await aiosqlite.connect(self.db_name)

    async def execute(
        self, query: str, values: Tuple = (), *, fetch: str = None, commit: bool = False,
        conn: aiosqlite.Connection = None
    ) -> Optional[Any]:
        bypass = conn
        conn = await self.connect() if conn is None else conn
        cursor = await conn.cursor()

        await cursor.execute(query, values)
        if fetch is not None:
            data = await self._fetch(cursor, fetch)
        else:
            data = None

        if commit:
            await conn.commit()

        await cursor.close()
        if bypass is None:
            await conn.close()

        return data

    async def run(self, query: str, values: Tuple = (), *, conn: aiosqlite.Connection = None) -> None:
        await self.execute(query, values, commit=True, conn=conn)
