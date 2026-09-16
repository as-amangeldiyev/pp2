"""Examples of a child class overriding a parent method."""


class Vehicle:
    def move(self):
        return "The vehicle moves."


class Bicycle(Vehicle):
    def move(self):
        return "The bicycle moves by pedaling."


bicycle = Bicycle()
print(bicycle.move())
