import json, logging, os, argparse
from etl.config import XML_INPUT, JSON_OUTPUT, ETL_LOG, DEAD_LETTER
from etl.parse_xml import parse_sms_records
from etl.clean_normalize import clean_record
from etl.categorize import categorize
from etl.load_db import get_conn, create_tables, upsert

os.makedirs(DEAD_LETTER, exist_ok=True)
logging.basicConfig(filename=ETL_LOG, level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")


def run(xml_path: str):
    raw = parse_sms_records(xml_path)
    logging.info(f"Parsed {len(raw)} records")

    cleaned, dead = [], []
    for r in raw:
        try:
            c = clean_record(r)
            c["category"] = categorize(c["body"])
            cleaned.append(c)
        except Exception as e:
            logging.warning(f"Dead letter: {e} | {r}")
            dead.append(r)

    if dead:
        with open(f"{DEAD_LETTER}/dead.json", "w") as f:
            json.dump(dead, f, indent=2)

    conn = get_conn()
    create_tables(conn)
    upsert(conn, cleaned)
    logging.info(f"Loaded {len(cleaned)} records into DB")

    # Export dashboard JSON
    from collections import Counter
    by_cat = Counter(c["category"] for c in cleaned)
    total_amount = sum(c["amount"] or 0 for c in cleaned)
    dashboard = {
        "total": len(cleaned),
        "total_amount": round(total_amount, 2),
        "by_category": dict(by_cat),
        "transactions": [
            {"date": c["date"], "type": c["category"], "amount": c["amount"], "party": c["address"]}
            for c in cleaned
        ]
    }
    os.makedirs(os.path.dirname(JSON_OUTPUT), exist_ok=True)
    with open(JSON_OUTPUT, "w") as f:
        json.dump(dashboard, f, indent=2)
    logging.info(f"Exported dashboard JSON to {JSON_OUTPUT}")
    print(f"Done. {len(cleaned)} records processed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--xml", default=XML_INPUT)
    args = ap.parse_args()
    run(args.xml)
