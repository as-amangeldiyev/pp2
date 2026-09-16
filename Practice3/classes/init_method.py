"""Examples of the __init__ constructor and instance properties."""


class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def introduce(self):
        return f"I am {self.name} in grade {self.grade}."


student = Student("Miras", 10)
print(student.introduce())

del student.grade
print("Grade property exists:", hasattr(student, "grade"))
