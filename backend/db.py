from os import get_blocking
import sqlite3


class Database():
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is not None:
            return self.connection
        try:
            return sqlite3.connect('callpicker_db.db')
        except Exception as e:
            print(e)

    def get_last_row(self):
        with self.get_connection() as cnx:
            with cnx.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stocks
                    (date text, trans text, symbol text, qty real, price real)
                ''')

            cursor.execute(
                "INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

            cnx.commit()
