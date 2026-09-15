"""Examples of positional and default function arguments."""


# Here is a function that accepts one positional and one default argument.
def calculate_total(price, quantity=1):
    return price * quantity


# Here is a positional call and a call that uses the default quantity.
print("Three notebooks:", calculate_total(450, 3))
print("One pen:", calculate_total(120))
