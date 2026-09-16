"""Examples of defining a class, creating an object, and using a method."""


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def description(self):
        return f"{self.title} by {self.author}"


favorite_book = Book("Abai Zholy", "Mukhtar Auezov")
print(favorite_book.description())
