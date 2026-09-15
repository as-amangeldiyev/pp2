"""Examples of a child class inheriting parent behavior."""


# Here is a parent Animal class and a Dog child class.
class Animal:
    def eat(self):
        return "The animal is eating."


class Dog(Animal):
    def bark(self):
        return "The dog says woof!"


# Here is a child object using both inherited and child methods.
pet_dog = Dog()
print(pet_dog.eat())
print(pet_dog.bark())
