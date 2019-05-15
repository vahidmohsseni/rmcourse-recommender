import sqlite3


def init_database():
    with sqlite3.connect("../database/db") as conn:
        conn.execute('''CREATE TABLE questions
                     (id integer PRIMARY KEY Autoincrement,
                     stack_id integer not null,
                     ans_id integer not null,
                     ans_tags text not null,
                     q_tags text not null)''')
        conn.commit()

        conn.execute('''CREATE TABLE worker
                     (id integer primary key autoincrement ,
                     stack_id integer not null,
                     tags text not null)''')
        conn.commit()


if __name__ == '__main__':
    init_database()