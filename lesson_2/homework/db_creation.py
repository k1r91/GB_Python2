import sqlite3,os

db_name = 'base.db3'
if os.path.exists(db_name):
    os.remove(db_name)
with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    queries =['''CREATE TABLE IF NOT EXISTS terminal (
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

            '''CREATE TABLE IF NOT EXISTS payment (
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
            FOREIGN KEY(agent_id) REFERENCES partner(id))'''
            ]
    for query in queries:
        cursor.execute(query)