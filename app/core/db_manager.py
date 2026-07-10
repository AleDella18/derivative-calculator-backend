import libsql
import os


class DBManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = libsql.connect(
                database=os.environ["TURSO_DATABASE_URL"],
                auth_token=os.environ["TURSO_AUTH_TOKEN"],
            )

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute(self, query, params=None):
        if self.conn is None:
            raise RuntimeError("Database not connected")

        if params is None:
            params = []

        return self.conn.execute(query, params)

    def commit(self):
        if self.conn is None:
            raise RuntimeError("Database not connected")
        self.conn.commit()