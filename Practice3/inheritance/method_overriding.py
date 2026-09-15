"""Examples of a child class overriding a parent method."""


# Here is a parent method and a child method with the same name but different behavior.
class Vehicle:
    def move(self):
        return "The vehicle moves."


class Bicycle(Vehicle):
    def move(self):
        return "The bicycle moves by pedaling."


# Here is an overridden method called on a Bicycle object.
bicycle = Bicycle()
print(bicycle.move())
