import json
import re
from pathlib import Path


PRICE_PATTERN = re.compile(r"(?<![\w.])(?:\d{1,3}(?:[ ,]\d{3})+|\d+)(?:[.,]\d{2})(?!\d)")
ITEM_PATTERN = re.compile(
    r"^\s*(?P<name>[A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё0-9 %'()./-]*?)"
    r"\s{2,}(?P<quantity>\d+(?:[.,]\d+)?\s*(?:kg|g|pcs?)?)"
    r"\s{2,}(?P<price>(?:\d{1,3}(?:[ ,]\d{3})+|\d+)[.,]\d{2})\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def amount(value: str) -> float:
    normalized = value.replace(" ", "")
    if "." in normalized:
        normalized = normalized.replace(",", "")
    else:
        normalized = normalized.replace(",", ".")
    return float(normalized)


def parse_receipt(text: str) -> dict:
    items = [
        {
            "name": match.group("name").strip(),
            "quantity": match.group("quantity").strip(),
            "price": amount(match.group("price")),
        }
        for match in ITEM_PATTERN.finditer(text)
    ]

    date_match = re.search(r"(?im)^\s*Date\s*:\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})", text)
    time_match = re.search(r"(?im)^\s*Time\s*:\s*(\d{1,2}:\d{2}(?::\d{2})?)", text)
    total_match = re.search(
        r"(?im)^\s*TOTAL\s*:\s*((?:\d{1,3}(?:[ ,]\d{3})+|\d+)[.,]\d{2})",
        text,
    )
    discount_match = re.search(
        r"(?im)^\s*Discount\s*:\s*((?:\d{1,3}(?:[ ,]\d{3})+|\d+)[.,]\d{2})",
        text,
    )
    payment_match = re.search(r"(?im)^\s*Payment\s+method\s*:\s*(.+?)\s*$", text)
    prices = [item["price"] for item in items]
    money_row = re.compile(r"(?im)^\s*(?:Subtotal|Discount|TOTAL)\s*:\s*(.+)$")
    prices.extend(
        amount(match.group())
        for row in money_row.findall(text)
        for match in PRICE_PATTERN.finditer(row)
    )

    calculated_subtotal = round(sum(item["price"] for item in items), 2)
    discount = amount(discount_match.group(1)) if discount_match else 0.0
    calculated_total = round(calculated_subtotal - discount, 2)

    return {
        "prices": prices,
        "products": items,
        "calculated_subtotal": calculated_subtotal,
        "discount": discount,
        "calculated_total": calculated_total,
        "receipt_total": amount(total_match.group(1)) if total_match else None,
        "date": date_match.group(1) if date_match else None,
        "time": time_match.group(1) if time_match else None,
        "payment_method": payment_match.group(1).strip() if payment_match else None,
    }


if __name__ == "__main__":
    receipt_path = Path(__file__).with_name("raw.txt")
    result = parse_receipt(receipt_path.read_text(encoding="utf-8"))
    print(json.dumps(result, indent=2, ensure_ascii=False))
