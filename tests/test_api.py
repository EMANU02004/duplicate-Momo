import sqlite3, pytest
from fastapi.testclient import TestClient
from api.app import app
import api.db as api_db


@pytest.fixture(autouse=True)
def override_db(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT, date TEXT, body TEXT UNIQUE,
            amount REAL, category TEXT
        )
    """)
    conn.executemany(
        "INSERT INTO transactions (address, date, body, amount, category) VALUES (?,?,?,?,?)",
        [
            ("+250780000001", "2023-11-14 12:00:00", "You received 5,000 RWF", 5000.0, "incoming_money"),
            ("+250780000002", "2023-11-14 13:00:00", "Payment of 500 RWF",     500.0,  "payment"),
        ]
    )
    conn.commit()
    monkeypatch.setattr(api_db, "get_conn", lambda: conn)
    yield
    conn.close()


client = TestClient(app)


def test_get_transactions():
    r = client.get("/transactions")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert data[0]["category"] == "incoming_money"


def test_get_transactions_limit():
    r = client.get("/transactions?limit=1")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_get_analytics():
    r = client.get("/analytics")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 2
    assert body["total_amount"] == 5500.0
    assert body["by_category"]["incoming_money"] == 1
    assert body["by_category"]["payment"] == 1
