import contextlib
import os
import sqlite3

from src import const

DB_NAME = os.path.join(const.DATA_DIR, "controlcentrum")

TABLE_CONTROL_UNITS = "control_units"
TABLE_MEASUREMENTS = "measurements"

TABLE_CONTROL_UNITS_DEFINITION = "(id INTEGER PRIMARY KEY, device_id INTEGER UNIQUE, name STRING, color STRING, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"


def init():
    create_table(TABLE_CONTROL_UNITS, TABLE_CONTROL_UNITS_DEFINITION)


def create_table(name, columns):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {name} {columns}")
        conn.commit()


def insert(table, columns, values):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        sql = f"INSERT INTO {table} {columns} VALUES {values}"
        # print("sql:", sql)
        cur.execute(sql)
        conn.commit()
        # except sqlite3.IntegrityError as e:
        #     print(e)


def update(table, values, where):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        sql = f"UPDATE {table} SET {values} WHERE {where}"
        # print("sql:", sql)
        cur.execute(sql)
        conn.commit()


def select_all(table):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()


def select_columns(table, columns, where):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        sql = f"SELECT {columns} FROM {table} WHERE {where}"
        # print("sql:", sql)
        cur.execute(sql)
        return cur.fetchall()

"""
init()
insert(TABLE_CONTROL_UNITS, "(unit_id, name, color)", "(5,'my_unit','blue')")
"""