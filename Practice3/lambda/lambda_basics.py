"""Examples of a lambda expression and an equivalent regular function."""


# Here is a regular function that doubles a number.
def double_number(number):
    return number * 2


# Here is an anonymous lambda that performs the same quick operation.
double_with_lambda = lambda number: number * 2
print("Regular function:", double_number(6))
print("Lambda function:", double_with_lambda(6))
