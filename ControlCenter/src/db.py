import contextlib
import os
import sqlite3

from src import const

DB_NAME = os.path.join(const.DATA_DIR, "controlcentrum")

TABLE_CONTROL_UNITS = "control_units"
TABLE_MEASUREMENTS = "measurements"

TABLE_CONTROL_UNITS_DEFINITION = "(id INTEGER PRIMARY KEY, unit_id INTEGER UNIQUE, name STRING, color STRING, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"


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
        try:
            cur.execute(f"INSERT INTO {table} {columns} VALUES {values}")
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(e)


def select(table):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()


"""
init()
insert(TABLE_CONTROL_UNITS, "(unit_id, name, color)", "(5,'my_unit','blue')")
"""