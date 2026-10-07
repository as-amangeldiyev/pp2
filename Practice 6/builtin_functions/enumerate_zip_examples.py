names = ["Ali", "Dana", "Mira"]
scores = [90, 85, 100]

# enumerate() gives each item an index.
for index, name in enumerate(names, start=1):
    print(index, name)

# zip() pairs items from two lists.
for name, score in zip(names, scores):
    print(name, "scored", score)

# Type checking and common type conversions.
value = "42"
number = int(value)
decimal_number = float(value)
text = str(number)
values = list((1, 2, 3))
print("type:", type(value), type(number), type(decimal_number))
print("Conversions:", number, decimal_number, text, values)
print("bool conversion:", bool(number))
