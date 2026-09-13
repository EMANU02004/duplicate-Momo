import os, textwrap, tempfile
from etl.parse_xml import parse_sms_records


def _write_xml(content: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False, mode="w") as f:
        f.write(content)
        return f.name


def test_parse_returns_records():
    path = _write_xml(textwrap.dedent("""\
        <?xml version="1.0"?>
        <smses>
          <sms address="250780000000" date="1700000000000" body="You have received 5,000 RWF" />
        </smses>
    """))
    records = parse_sms_records(path)
    os.unlink(path)
    assert len(records) == 1
    assert records[0]["address"] == "250780000000"

def test_parse_empty_smses():
    path = _write_xml('<?xml version="1.0"?><smses></smses>')
    records = parse_sms_records(path)
    os.unlink(path)
    assert records == []

def test_parse_multiple_records():
    path = _write_xml(textwrap.dedent("""\
        <?xml version="1.0"?>
        <smses>
          <sms address="250780000001" date="1700000000000" body="You have received 1,000 RWF" />
          <sms address="250780000002" date="1700000001000" body="Payment of 500 RWF" />
        </smses>
    """))
    records = parse_sms_records(path)
    os.unlink(path)
    assert len(records) == 2
    assert records[1]["address"] == "250780000002"

def test_parse_missing_attribute():
    path = _write_xml(textwrap.dedent("""\
        <?xml version="1.0"?>
        <smses>
          <sms date="1700000000000" body="You have received 1,000 RWF" />
        </smses>
    """))
    records = parse_sms_records(path)
    os.unlink(path)
    assert records[0]["address"] == ""
