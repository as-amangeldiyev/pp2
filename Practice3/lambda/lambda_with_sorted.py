"""Examples of custom sorting with a lambda key."""


# Here is a list of products sorted by the price stored in each dictionary.
products = [
    {"name": "Notebook", "price": 850},
    {"name": "Pen", "price": 120},
    {"name": "Backpack", "price": 5000},
]
products_by_price = sorted(products, key=lambda product: product["price"])
print("Products by price:", products_by_price)
