class Animal:
    def __init__(self, species):
        self.species = species

class Dog(Animal):
    def __init__(self, name, breed):
        # Call Animal's __init__ to set species="Canine"
        super().__init__(species="Canine") 
        self.name = name
        self.breed = breed

dog = Dog("Buddy", "Golden Retriever")
print(dog.species)  # Output: Canine
print(dog.name)     # Output: Buddy