import os
import sqlite3

from terminal import PaymentTerminal
from DB import Sqlite3Db as DB, DatabaseNotFoundException


class Controller:

    def __init__(self):
        if not os.path.exists(DB.DB_NAME):
            raise DatabaseNotFoundException(DB.DB_NAME)
        self.db_name = DB.DB_NAME

    def get_terminals(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT * FROM terminal").fetchall()



def test_main():
    controller = Controller()
    print(controller.get_terminals())

if __name__ == '__main__':
    test_main()