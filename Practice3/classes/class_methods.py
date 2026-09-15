"""Examples of an instance method that changes an object property."""


# Here is a class with methods that read and update an account balance.
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance


# Here is an object property modified through an instance method.
account = BankAccount("Amina", 1000)
print("New balance:", account.deposit(500))
