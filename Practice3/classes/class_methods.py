"""Examples of an instance method that changes an object property."""


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance


account = BankAccount("Amina", 1000)
print("New balance:", account.deposit(500))
