"""Examples of calling a parent constructor with super()."""


class Person:
    def __init__(self, name):
        self.name = name


class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def introduce(self):
        return f"{self.name} teaches {self.subject}."


teacher = Teacher("Zhanar", "Mathematics")
print(teacher.introduce())
