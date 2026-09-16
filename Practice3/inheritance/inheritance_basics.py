"""Examples of a child class inheriting parent behavior."""


class Animal:
    def eat(self):
        return "The animal is eating."


class Dog(Animal):
    def bark(self):
        return "The dog says woof!"


pet_dog = Dog()
print(pet_dog.eat())
print(pet_dog.bark())
