n = int(input("Enter N: "))

# Squares from 0 through n.
square_numbers = (number**2 for number in range(n + 1))
print("Squares:", list(square_numbers))

# Even numbers from 0 through n, separated by commas.
even_numbers = (number for number in range(n + 1) if number % 2 == 0)
print("Even numbers:", ", ".join(map(str, even_numbers)))

# Numbers from 0 through n that are divisible by 3 and 4.
divisible_numbers = (
    number for number in range(n + 1) if number % 3 == 0 and number % 4 == 0
)
print("Divisible by 3 and 4:", list(divisible_numbers))

# Squares from a through b.
a = int(input("Enter the first number: "))
b = int(input("Enter the last number: "))
squares = (number**2 for number in range(a, b + 1))
for square in squares:
    print(square)

# Numbers from n down to 0.
n = int(input("Enter a number to count down from: "))
countdown = (number for number in range(n, -1, -1))
for number in countdown:
    print(number)
