from lxml import etree


def parse_sms_records(xml_path: str) -> list[dict]:
    tree = etree.parse(xml_path)
    records = []
    for sms in tree.findall(".//sms"):
        records.append({
            "address": sms.get("address", ""),
            "date":    sms.get("date", ""),
            "body":    sms.get("body", ""),
        })
    return records
