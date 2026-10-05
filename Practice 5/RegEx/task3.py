import re


text = "IDs: A12, B345, and C6. Dates: 2026-10-05 and 2025-01-02."
patterns = {
    "exactly two digits": r"\b\d{2}\b",
    "at least two digits": r"\b\d{2,}\b",
    "two to four digits": r"\b\d{2,4}\b",
    "uppercase initial plus digits": r"\b[A-Z]\d+\b",
    "ISO dates": r"\b\d{4}-\d{2}-\d{2}\b",
}

for label, pattern in patterns.items():
    print(f"{label}: {re.findall(pattern, text)}")
