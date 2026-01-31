import sqlite3
from typing import Optional

from soar.modules.database.database_interface import DatabaseInterface


class SqliteDatabase(DatabaseInterface):
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None

    def _connect(self):
        self._connection = sqlite3.connect(self._db_path)

    def disconnect(self):
        if self._connection:
            self._connection.close()

    def execute(self, query: str, params: tuple = ()):
        if not self._connection:
            self._connect()

        self._connection.execute(query, params)

    def fetch_one(self, query: str, params: tuple = ()):
        if not self._connection:
            self._connect()

        res = self._connection.execute(query, params)
        return res.fetchone()

    def fetch_all(self, query: str, params: tuple = ()):
        if not self._connection:
            self._connect()

        res = self._connection.execute(query, params)
        return res.fetchall()

    def commit(self):
        if self._connection:
            self._connection.commit()

    def rollback(self):
        if self._connection:
            self._connection.rollback()
