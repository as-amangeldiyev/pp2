"""Examples of inheriting features from more than one parent class."""


class Camera:
    def take_photo(self):
        return "Photo taken."


class Phone:
    def make_call(self):
        return "Calling a contact."


class Smartphone(Camera, Phone):
    pass


smartphone = Smartphone()
print(smartphone.take_photo())
print(smartphone.make_call())
