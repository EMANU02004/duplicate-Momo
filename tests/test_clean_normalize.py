from etl.clean_normalize import normalize_amount, normalize_phone, normalize_date, clean_record


def test_normalize_amount():
    assert normalize_amount("You received 5,000 RWF") == 5000.0

def test_normalize_amount_none():
    assert normalize_amount("Your OTP is ABC") is None

def test_normalize_phone():
    assert normalize_phone("250780000000") == "+250780000000"

def test_normalize_phone_with_dashes():
    assert normalize_phone("+250-78-000-0000") == "+25078000000"

def test_normalize_date_valid():
    result = normalize_date("2023-11-14 12:00:00")
    assert result == "2023-11-14 12:00:00"

def test_normalize_date_invalid():
    result = normalize_date("not-a-date")
    assert result == "not-a-date"

def test_clean_record():
    record = {"address": "250780000000", "date": "2023-11-14 12:00:00", "body": "  You received 5,000 RWF  "}
    result = clean_record(record)
    assert result["address"] == "+250780000000"
    assert result["amount"] == 5000.0
    assert result["body"] == "You received 5,000 RWF"
