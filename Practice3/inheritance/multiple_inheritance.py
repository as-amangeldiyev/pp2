"""Examples of inheriting features from more than one parent class."""


# Here is a class that combines capabilities from two parent classes.
class Camera:
    def take_photo(self):
        return "Photo taken."


class Phone:
    def make_call(self):
        return "Calling a contact."


class Smartphone(Camera, Phone):
    pass


# Here is one object using methods inherited from both parents.
smartphone = Smartphone()
print(smartphone.take_photo())
print(smartphone.make_call())
