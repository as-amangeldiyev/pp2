import math
import random


def main():
    values = [-8, 3, 12, 4]
    print("min / max:", min(values), max(values))
    print("abs(-8):", abs(-8))
    print("round(3.14159, 2):", round(3.14159, 2))
    print("pow(2, 5):", pow(2, 5))

    print("sqrt(81):", math.sqrt(81))
    print("ceil(4.2) / floor(4.8):", math.ceil(4.2), math.floor(4.8))
    print("sin(pi / 2) / cos(0):", math.sin(math.pi / 2), math.cos(0))
    print("pi / e:", math.pi, math.e)

    random.seed(7)  # Fixed seed makes this demonstration reproducible.
    print("random():", random.random())
    print("randint(1, 10):", random.randint(1, 10))
    print("choice:", random.choice(["red", "green", "blue"]))
    cards = ["ace", "king", "queen", "jack"]
    random.shuffle(cards)
    print("shuffled cards:", cards)


if __name__ == "__main__":
    main()
