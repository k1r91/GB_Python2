import os
import sqlite3

from terminal import PaymentTerminal
from DB import Sqlite3Db as DB, DatabaseNotFoundException


class Controller:

    def __init__(self):
        if not os.path.exists(DB.DB_NAME):
            raise DatabaseNotFoundException(DB.DB_NAME)
        self.db_name = DB.DB_NAME

    def get_table_info(self, table):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            headers = cursor.execute("PRAGMA TABLE_INFO({})"
                                     .format(table)).fetchall()
            titles = [item[1] for item in headers]
            data = cursor.execute("SELECT * FROM {}".format(table)).fetchall()
            result = data
            result.insert(0, tuple(titles))
            return result

    def delete_from(self, table, id):
        '''
        removes database record with appropriate id
        :param table:
        :param id:
        :return:
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            r = cursor.execute('DELETE FROM {} WHERE id=?'.format(table),
                               (id, ))

    def update(self, table, data, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if table is 'terminal':
                query = '''UPDATE terminal SET id=?, configuration=?,
                        title=?, comment=?, pub_key=? WHERE id=?'''
                cursor.execute(query, (data[0], data[1],data[2],
                                       data[3], data[4], id, ))
            elif table is 'partner':
                query = '''UPDATE partner SET id=?, title=?,
                        comment=? WHERE id=?'''
                cursor.execute(query, (data[0], data[1], data[2], id, ))

    def get_fun(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            data = cursor.execute("SELECT * FROM terminal LIMIT 2 OFFSET 1").fetchall()
            cursor.execute("UPDATE terminal SET id=286 WHERE id=324")


def test_main():
    controller = Controller()
    print(controller.get_table_info('terminal'))
    print(controller.get_table_info('partner'))
    #print(controller.get_fun())

if __name__ == '__main__':
    test_main()