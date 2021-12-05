import sqlite3
import contextlib

class Provider:

    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        return conn, c

    def return_connection(self, conn):
        conn.close()

    @contextlib.contextmanager
    def read(self):
        try:
            conn, c = self.get_connection()
            yield conn, c
        finally:
            self.return_connection(conn)

    @contextlib.contextmanager
    def write(self):
        try:
            conn, c = self.get_connection()
            yield conn, c
            conn.commit()
        finally:
            self.return_connection(conn)
    