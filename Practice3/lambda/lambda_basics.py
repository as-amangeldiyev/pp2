"""Examples of a lambda expression and an equivalent regular function."""


def double_number(number):
    return number * 2


double_with_lambda = lambda number: number * 2
print("Regular function:", double_number(6))
print("Lambda function:", double_with_lambda(6))
