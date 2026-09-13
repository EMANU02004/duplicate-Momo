from fastapi import FastAPI
from api.db import get_conn
from api.schemas import Transaction, Analytics

app = FastAPI(title="MoMo API")


@app.get("/transactions", response_model=list[Transaction])
def get_transactions(limit: int = 100, offset: int = 0):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, address, date, amount, category FROM transactions LIMIT ? OFFSET ?",
        (limit, offset)
    ).fetchall()
    return [dict(r) for r in rows]


@app.get("/analytics", response_model=Analytics)
def get_analytics():
    conn = get_conn()
    rows = conn.execute("SELECT category, COUNT(*) as cnt, SUM(amount) as total FROM transactions GROUP BY category").fetchall()
    by_cat = {r["category"]: r["cnt"] for r in rows}
    total = sum(r["cnt"] for r in rows)
    total_amount = sum(r["total"] or 0 for r in rows)
    return {"total": total, "total_amount": round(total_amount, 2), "by_category": by_cat}
