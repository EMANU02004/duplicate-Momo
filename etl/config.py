import os

XML_INPUT   = os.getenv("XML_INPUT",   "data/raw/momo.xml")
DB_PATH     = os.getenv("DATABASE_URL", "data/db.sqlite3")
JSON_OUTPUT = os.getenv("JSON_OUTPUT",  "data/processed/dashboard.json")
ETL_LOG     = "data/logs/etl.log"
DEAD_LETTER = "data/logs/dead_letter"

CATEGORIES = {
    "incoming_money":        ["received"],
    "payment":               ["payment", "paid to", "bank charge"],
    "transfer":              ["transferred to", "transfer to"],
    "withdrawal":            ["withdrawn", "cash out", "agent"],
    "airtime":               ["airtime", "bundle"],
    "third_party_initiated": ["initiated by"],
}
