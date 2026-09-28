class CountUp:
    """A small custom iterator yielding integers from start through stop."""

    def __init__(self, start, stop):
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def count_up(start, stop):
    """A generator function: yield pauses and resumes the function."""
    current = start
    while current <= stop:
        yield current
        current += 1


def fibonacci(limit):
    """Yield the Fibonacci numbers that do not exceed limit."""
    previous, current = 0, 1
    while previous <= limit:
        yield previous
        previous, current = current, previous + current


def main():
    numbers = iter([10, 20, 30])
    print("Manual iter()/next():", next(numbers), next(numbers), next(numbers))

    print("Custom iterator:", list(CountUp(1, 5)))
    print("Loop through iterator:")
    for number in CountUp(1, 3):
        print(number)

    print("Generator function:", list(count_up(2, 6)))
    print("Fibonacci generator:", list(fibonacci(20)))

    # Generator expressions are lazy: values are calculated as they are read.
    squares = (number * number for number in range(1, 6))
    print("Generator expression:", list(squares))


if __name__ == "__main__":
    main()
