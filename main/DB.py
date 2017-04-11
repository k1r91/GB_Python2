import sqlite3
import os


class Sqlite3Db:

    DB_NAME = 'base.db3'

    def flush(self):
        if os.path.exists(self.DB_NAME):
            os.remove(self.DB_NAME)
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            queries =['''CREATE TABLE terminal (
                    id INTEGER,
                    configuration TEXT,
                    title TEXT,
                    comment TEXT,
                    pub_key INTEGER,
                    PRIMARY KEY(id))''',

                    '''CREATE TABLE partner (
                    id INTEGER,
                    title TEXT,
                    comment TEXT,
                    PRIMARY KEY(id))''',

                    '''CREATE TABLE payment (
                    id INTEGER AUTO_INCREMENT,
                    datetime DATE,
                    terminal_id INTEGER,
                    transaction_id INTEGER,
                    partner_id INTEGER,
                    summ INTEGER,
                    PRIMARY KEY(id),
                    FOREIGN KEY(terminal_id) REFERENCES terminal(id),
                    FOREIGN KEY(partner_id) REFERENCES partner(id))''',

                    '''CREATE TABLE credit(
                    id INTEGER AUTO_INCREMENT,
                    agent_id INTEGER,
                    datetime DATE,
                    summ INTEGER,
                    FOREIGN KEY(agent_id) REFERENCES partner(id))''',

                    '''CREATE TABLE debit(
                    id INTEGER AUTO_INCREMENT,
                    agent_id INTEGER,
                    datetime DATE,
                    summ INTEGER,
                    FOREIGN KEY(agent_id) REFERENCES partner(id))''',

                    '''INSERT INTO terminal (id, configuration, title,
                    comment, pub_key) VALUES
                    (324, "conf/terminal_324", "Терминал № 324", "", 4569872583654715),
                    (825, "conf/terminal_825", "Терминал № 825", "", 9548732164895246),
                    (927, "conf/terminal_927", "Терминал № 927", "", 6812649873541549)''',

                    '''INSERT INTO partner (id, title, comment) VALUES
                    (1, "Магнит", ""),
                    (2, "X5 Retail Group", ""),
                    (3, "Сургутнефтегаз", ""),
                    (4, "Лукойл", ""),
                    (5, "Evraz", ""),
                    (6, "Группа УГМК", ""),
                    (7, "Норильский никель", ""),
                    (8, "МТС", ""),
                    (9, "Татнефть", ""),
                    (10, "Мечел", "")'''
                    ]
            for query in queries:
                cursor.execute(query)


class DatabaseNotFoundException(Exception):

    def __init__(self, db_name):
        super().__init__(self)
        self.db_name = db_name

    def __str__(self):
        return 'Database {} not found'.format(self.db_name)


def main():
    db = DB()
    db.flush()

if __name__ == '__main__':
    main()