import sqlite3

import stock_helper
from constants import path_to_db
from sqlite3 import Error


def before_start():
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       userid INT PRIMARY KEY,
       securities TEXT,
       last_date TEXT);
    """)

    conn.commit()
    conn.close()


def set_user(user_id, securities, last_date):
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    txt = " ".join(securities)  # securities is array
    user = (user_id, txt, str(last_date))
    try:
        cur.execute("INSERT INTO users VALUES(?, ?, ?);", user)
    except Error as e:
        sql = '''
            UPDATE users
            SET securities = ?,
                last_date = ?
            WHERE userid = ?
        '''
        cur.execute(sql, (txt, str(last_date), user_id))
    conn.commit()
    conn.close()


def update_user_date(user_id, last_date):
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    user = (user_id, "", str(last_date))
    try:
        cur.execute("INSERT INTO users VALUES(?, ?, ?);", user)
    except Error as e:
        sql = '''
                UPDATE users
                SET last_date = ?
                WHERE userid = ?
            '''
        cur.execute(sql, (str(last_date), user_id))
    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    conn.commit()
    sql = "SELECT * FROM users WHERE userid=?"
    cur.execute(sql, (user_id,))

    rows = cur.fetchall()

    if len(rows) != 1:
        return -1

    return rows[0]


def get_all():
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    conn.commit()
    sql = "SELECT userid, securities, last_date FROM users"
    cur.execute(sql, ())
    rows = cur.fetchall()
    return rows


def refresh():
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    conn.commit()
    sqlite_select_query = """SELECT * FROM users"""
    cur.execute(sqlite_select_query)
    rows = cur.fetchall()
    print(rows)
    for v in rows:
        a, b, c = v
        ls = []
        if len(b) != 0:
            ls = b.split(" ")
        ls = list(set(ls))
        good = []
        for x in ls:
            if stock_helper.exist(x):
                good.append(x)
        set_user(a, good, c)
    return rows
