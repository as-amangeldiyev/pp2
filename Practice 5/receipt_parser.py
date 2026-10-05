import argparse
import json
import re
from pathlib import Path


MONEY = r"(?:\d{1,3}(?:[ \u00a0]\d{3})+|\d+)[.,]\d{2}"
ITEM_START = re.compile(r"^\s*(\d+)\.\s*$")
SALE_LINE = re.compile(
    rf"^\s*(?P<quantity>\d+(?:[.,]\d+)?)\s*[xх]\s*"
    rf"(?P<unit_price>{MONEY})\s*$",
    re.IGNORECASE,
)


def parse_amount(value: str) -> float:
    """Convert a receipt amount such as '1 200,00' to a number."""
    return float(value.replace("\u00a0", "").replace(" ", "").replace(",", "."))


def parse_receipt(text: str) -> dict:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    products = []

    index = 0
    while index < len(lines):
        start = ITEM_START.match(lines[index])
        if not start:
            index += 1
            continue

        # Receipt products span four lines: item number, name, quantity x price,
        # then the line total (also repeated after the word "Стоимость").
        if index + 3 < len(lines):
            name = lines[index + 1].strip()
            sale = SALE_LINE.match(lines[index + 2])
            line_total_match = re.fullmatch(rf"\s*({MONEY})\s*", lines[index + 3])
            if name and sale and line_total_match:
                products.append(
                    {
                        "number": int(start.group(1)),
                        "name": name,
                        "quantity": float(sale.group("quantity").replace(",", ".")),
                        "unit_price": parse_amount(sale.group("unit_price")),
                        "total": parse_amount(line_total_match.group(1)),
                    }
                )
                index += 4
                continue
        index += 1

    # Keep every monetary amount in receipt order, including repeated line
    # totals, the card payment, the final total, and VAT amount.
    prices = [parse_amount(match.group()) for match in re.finditer(MONEY, text)]

    total_match = re.search(rf"(?im)^\s*ИТОГО\s*:\s*({MONEY})", text)
    date_time_match = re.search(
        r"(?im)^\s*Время\s*:\s*(\d{1,2}\.\d{1,2}\.\d{4})\s+"
        r"(\d{1,2}:\d{2}:\d{2})",
        text,
    )
    payment_match = re.search(r"(?im)^\s*(Банковская карта)\s*:", text)

    return {
        "prices": prices,
        "products": products,
        "calculated_total": round(sum(product["total"] for product in products), 2),
        "receipt_total": parse_amount(total_match.group(1)) if total_match else None,
        "date": date_time_match.group(1) if date_time_match else None,
        "time": date_time_match.group(2) if date_time_match else None,
        "payment_method": payment_match.group(1) if payment_match else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a WEBKASSA receipt text file.")
    parser.add_argument("receipt", type=Path, help="path to the receipt text file")
    args = parser.parse_args()
    result = parse_receipt(args.receipt.read_text(encoding="utf-8"))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
