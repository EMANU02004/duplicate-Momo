from etl.categorize import categorize


def test_incoming_money():
    assert categorize("You have received 5,000 RWF from John") == "incoming_money"

def test_incoming_money_case_insensitive():
    assert categorize("You Have RECEIVED 5,000 RWF") == "incoming_money"

def test_payment():
    assert categorize("Payment of 1,000 RWF to Shop") == "payment"

def test_payment_paid_to():
    assert categorize("You paid to Kigali Store 2,000 RWF") == "payment"

def test_transfer():
    assert categorize("You have transferred to 0780000000") == "transfer"

def test_withdrawal():
    assert categorize("You have withdrawn 10,000 RWF from agent") == "withdrawal"

def test_airtime():
    assert categorize("You have purchased airtime worth 500 RWF") == "airtime"

def test_third_party_initiated():
    assert categorize("Transaction initiated by merchant") == "third_party_initiated"

def test_other():
    assert categorize("Your OTP is 123456") == "other"

def test_empty_string():
    assert categorize("") == "other"
