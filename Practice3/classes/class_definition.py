"""Examples of defining a class, creating an object, and using a method."""


# Here is a class that represents a book and gives it an instance method.
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def description(self):
        return f"{self.title} by {self.author}"


# Here is an object created from the Book class.
favorite_book = Book("Abai Zholy", "Mukhtar Auezov")
print(favorite_book.description())
