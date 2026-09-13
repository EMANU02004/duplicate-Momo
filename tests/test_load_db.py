import sqlite3, pytest
from etl.load_db import create_tables, upsert


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    create_tables(c)
    yield c
    c.close()


def test_create_tables(conn):
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    assert any(t[0] == "transactions" for t in tables)


def test_upsert_inserts_record(conn):
    upsert(conn, [{"address": "+250780000000", "date": "2023-11-14 12:00:00",
                   "body": "You received 5,000 RWF", "amount": 5000.0, "category": "incoming_money"}])
    rows = conn.execute("SELECT * FROM transactions").fetchall()
    assert len(rows) == 1


def test_upsert_ignores_duplicate(conn):
    record = {"address": "+250780000000", "date": "2023-11-14 12:00:00",
              "body": "You received 5,000 RWF", "amount": 5000.0, "category": "incoming_money"}
    upsert(conn, [record])
    upsert(conn, [record])
    rows = conn.execute("SELECT * FROM transactions").fetchall()
    assert len(rows) == 1


def test_upsert_multiple_records(conn):
    records = [
        {"address": "+250780000001", "date": "2023-11-14 12:00:00",
         "body": "You received 1,000 RWF", "amount": 1000.0, "category": "incoming_money"},
        {"address": "+250780000002", "date": "2023-11-14 13:00:00",
         "body": "Payment of 500 RWF", "amount": 500.0, "category": "payment"},
    ]
    upsert(conn, records)
    rows = conn.execute("SELECT * FROM transactions").fetchall()
    assert len(rows) == 2
