import sqlite3
from etl.config import DB_PATH


def get_conn():
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            address  TEXT,
            date     TEXT,
            body     TEXT UNIQUE,
            amount   REAL,
            category TEXT
        )
    """)
    conn.commit()


def upsert(conn, records: list[dict]):
    conn.executemany("""
        INSERT OR IGNORE INTO transactions (address, date, body, amount, category)
        VALUES (:address, :date, :body, :amount, :category)
    """, records)
    conn.commit()
