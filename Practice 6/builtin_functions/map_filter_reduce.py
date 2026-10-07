from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map() changes every item; filter() keeps items matching a condition.
squared = list(map(lambda number: number * number, numbers))
even_numbers = list(filter(lambda number: number % 2 == 0, numbers))
total = reduce(lambda first, second: first + second, numbers)

print("Numbers:", numbers)
print("Squares:", squared)
print("Even numbers:", even_numbers)
print("Sum using reduce():", total)
print("len / sum / min / max:", len(numbers), sum(numbers), min(numbers), max(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))
