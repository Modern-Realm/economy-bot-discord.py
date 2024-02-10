import mysql.connector as mysql
import mysql.connector.pooling as mysql_pooling

from typing import Optional, Any, Tuple


class Database:
    def __init__(
        self, username: str, passwd: str, db_name: str,
        host: str = "localhost", port: int = 3306,
        pool_size: int = 10
    ):
        self._pool = mysql_pooling.MySQLConnectionPool(
            host=host, port=port, user=username, passwd=passwd, database=db_name,
            pool_size=pool_size
        )

    @staticmethod
    async def _fetch(cursor, mode: str) -> Optional[Any]:
        if mode == "one":
            return cursor.fetchone()
        if mode == "many":
            return cursor.fetchmany()
        if mode == "all":
            return cursor.fetchall()

        return None

    async def connect(self):
        return self._pool.get_connection()

    async def execute(
        self, query: str, values: Tuple = (), *, fetch: str = None, commit: bool = False,
        conn: mysql_pooling.PooledMySQLConnection = None
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

    async def run(self, query: str, values: Tuple = (), *, conn: mysql_pooling.PooledMySQLConnection = None) -> None:
        await self.execute(query, values, commit=True, conn=conn)
