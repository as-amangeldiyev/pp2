"""Examples of the __init__ constructor and instance properties."""


# Here is a class whose constructor gives every student individual data.
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def introduce(self):
        return f"I am {self.name} in grade {self.grade}."


# Here is an object that uses properties created by __init__.
student = Student("Miras", 10)
print(student.introduce())

# Here is an instance property deleted after the object has been created.
del student.grade
print("Grade property exists:", hasattr(student, "grade"))
