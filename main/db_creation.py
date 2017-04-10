import sqlite3, os

db_name = 'base.db3'
if os.path.exists(db_name):
    os.remove(db_name)
with sqlite3.connect(db_name) as conn:
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