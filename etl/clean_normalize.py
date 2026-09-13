import re
from dateutil import parser as dateparser


def normalize_amount(text: str) -> float | None:
    match = re.search(r"[\d,]+(?:\.\d+)?", text.replace(",", ""))
    return float(match.group().replace(",", "")) if match else None


def normalize_date(ms_timestamp: str) -> str:
    try:
        return dateparser.parse(ms_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ms_timestamp


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    return f"+{digits}" if digits else phone


def clean_record(record: dict) -> dict:
    return {
        "address": normalize_phone(record["address"]),
        "date":    normalize_date(record["date"]),
        "body":    record["body"].strip(),
        "amount":  normalize_amount(record["body"]),
    }
