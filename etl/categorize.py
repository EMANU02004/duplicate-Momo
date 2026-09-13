from etl.config import CATEGORIES


def categorize(body: str) -> str:
    lower = body.lower()
    for category, keywords in CATEGORIES.items():
        if any(kw in lower for kw in keywords):
            return category
    return "other"
