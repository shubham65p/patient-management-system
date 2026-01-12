import sqlite3

class SQLiteDatabase:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.cursor = conn.cursor()

    def execute(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)
        return self.cursor

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    @property
    def lastrowid(self):
        return self.cursor.lastrowid
    