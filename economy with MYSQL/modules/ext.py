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
        """
        creates a new pool connection to the database.
        """

        return self._pool.get_connection()

    async def execute(
        self, query: str, values: Tuple = (), *, fetch: str = None, commit: bool = False,
        conn: mysql_pooling.PooledMySQLConnection = None
    ) -> Optional[Any]:
        """
        runs the query without committing any changes to the database if `commit` is not passed at func call.

        Tip: use this method for fetching like:`SELECT` queries.

        :param query: SQL query.
        :param values: values to be passed to the query.
        :param fetch: Takes ('one', 'many', 'all').
        :param commit: Commits the changes to the database if it's set to `True`.
        :param conn: pass the new pool connection to execute two or more methods. If passed, you've to close it manually.
        :return: required data.
        """

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
        """
        runs the query and commits any changes to the database directly.

        Tip: use this method if you want to commit changes to the database. Like: `CREATE, UPDATE, INSERT, DELETE`, etc.

        :param query: SQL query
        :param values: values to be passed to the query.
        :param conn: pass the new pool connection to execute two or more methods. If passed, you've to close it manually.
        """

        await self.execute(query, values, commit=True, conn=conn)
