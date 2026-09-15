"""Examples of collecting extra positional and keyword arguments."""


# Here is a function that uses *args for items and **kwargs for order details.
def describe_order(*items, **details):
    item_list = ", ".join(items)
    customer = details.get("customer", "Guest")
    delivery = details.get("delivery", "standard")
    return f"{customer} ordered {item_list} with {delivery} delivery."


# Here is a call that supplies extra positional and keyword arguments.
print(describe_order("tea", "bread", customer="Dana", delivery="express"))
