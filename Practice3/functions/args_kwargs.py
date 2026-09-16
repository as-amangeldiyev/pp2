"""Examples of collecting extra positional and keyword arguments."""


def describe_order(*items, **details):
    item_list = ", ".join(items)
    customer = details.get("customer", "Guest")
    delivery = details.get("delivery", "standard")
    return f"{customer} ordered {item_list} with {delivery} delivery."


print(describe_order("tea", "bread", customer="Dana", delivery="express"))
