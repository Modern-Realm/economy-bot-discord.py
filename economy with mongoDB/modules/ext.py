from typing import Mapping, Any
from pymongo import MongoClient
from pymongo.database import Database as MongoDB
from pymongo.collection import Collection


class Database:
    def __init__(
        self, cluster_url: str, db_name: str, min_pool_size: int = 10, max_pool_size: int = 15
    ) -> None:
        self.cluster_url = cluster_url
        self.db_name = db_name

        self._conn = MongoClient(self.cluster_url, minPoolSize=min_pool_size, maxPoolSize=max_pool_size)

    @property
    def db(self) -> MongoDB[Mapping[str, Any]]:
        return self._conn[self.db_name]

    def cursor(self, table_name: str) -> Collection[Mapping[str, Any]]:
        return self.db[table_name]

    def __del__(self):
        self._conn.close()
