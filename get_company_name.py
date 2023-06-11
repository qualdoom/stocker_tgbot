import apimoex
import requests
import sqlite3

from constants import path_to_names


def table_exist():
    conn = sqlite3.connect(path_to_names)
    cur = conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='companies' ''')
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False


def before_start():
    conn = sqlite3.connect(path_to_names)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS companies(
               short_name TXT,
               full_name TXT);
            """)

    conn.commit()
    with requests.Session() as session:
        based = apimoex.get_board_securities(session)
        for v in based:
            name = (v['SECID'], v['SHORTNAME'])
            cur.execute("INSERT INTO companies VALUES(?, ?);", name)

    conn.commit()
    conn.close()


def get_name(company):
    company.strip()
    company.upper()
    if not table_exist():
        before_start()

    conn = sqlite3.connect(path_to_names)
    cur = conn.cursor()
    conn.commit()
    sql = "SELECT * FROM companies WHERE short_name=?"
    cur.execute(sql, (company,))

    rows = cur.fetchall()

    if len(rows) != 1:
        return -1

    a, b = rows[0]

    return b
