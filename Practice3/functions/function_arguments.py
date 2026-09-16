"""Examples of positional and default function arguments."""


def calculate_total(price, quantity=1):
    return price * quantity


print("Three notebooks:", calculate_total(450, 3))
print("One pen:", calculate_total(120))
