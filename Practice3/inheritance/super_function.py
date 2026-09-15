"""Examples of calling a parent constructor with super()."""


# Here is a child constructor that reuses parent initialization with super().
class Person:
    def __init__(self, name):
        self.name = name


class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def introduce(self):
        return f"{self.name} teaches {self.subject}."


# Here is a Teacher object with data initialized by both classes.
teacher = Teacher("Zhanar", "Mathematics")
print(teacher.introduce())
