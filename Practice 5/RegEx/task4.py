import re


text = "Warning: disk 8 is full.\nwarning: disk 9 is almost full."

print(re.findall(r"^warning:.*$", text, re.IGNORECASE | re.MULTILINE))
print(re.findall(r"disk\s+\d+", text, re.IGNORECASE))
print(re.findall(r"(?s)Warning:.*full\.", text))
