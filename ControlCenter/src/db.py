import contextlib
import os
import sqlite3

from src import const

DB_NAME = os.path.join(const.DATA_DIR, "controlcentrum")

TABLE_CONTROL_UNITS = "control_units"
TABLE_MEASUREMENTS = "measurements"

TABLE_CONTROL_UNITS_DEFINITION = "(id INTEGER PRIMARY KEY, device_id INTEGER UNIQUE, name STRING, color STRING, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"
TABLE_MEASUREMENTS_DEFINITION = "(id INTEGER PRIMARY KEY, device_id INTEGER, temperature INTEGER, light_intensity INTEGER, shutter_status INTEGER, from_history INTEGER, timestamp REAL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(device_id) REFERENCES control_units(device_id) )"


def init():
    # Enable foreign key constraints
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        conn.commit()

    create_table(TABLE_CONTROL_UNITS, TABLE_CONTROL_UNITS_DEFINITION)
    create_table(TABLE_MEASUREMENTS, TABLE_MEASUREMENTS_DEFINITION)


def create_table(name, columns):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {name} {columns}")
        conn.commit()


def insert(table, columns, values):
    """
    :throws: sqlite3.IntegrityError when UNIQUE constraint fails
    """
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        sql = f"INSERT INTO {table} {columns} VALUES {values}"
        cur.execute(sql)
        conn.commit()


def update(table, values, where):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        sql = f"UPDATE {table} SET {values} WHERE {where}"
        cur.execute(sql)
        conn.commit()


def select_all(table):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()


def select_columns(table, columns, where, orderby=None, size=None):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        sql = f"SELECT {columns} FROM {table} WHERE {where}"

        if orderby:
            sql += f" ORDER BY {orderby}"

        cur.execute(sql)
        if not size:
            return cur.fetchall()
        else:
            return cur.fetchmany(size)


def select_by_where(table, where):
    with contextlib.closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE {where}")
        return cur.fetchall()
