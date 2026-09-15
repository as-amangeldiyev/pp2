"""Examples of the difference between class and instance variables."""


# Here is a class variable shared by all objects and an instance variable unique to each object.
class ClubMember:
    club_name = "Python Club"

    def __init__(self, member_name):
        self.member_name = member_name


# Here is a demonstration that changing one instance does not change the class variable.
first_member = ClubMember("Ali")
second_member = ClubMember("Sara")
first_member.member_name = "Alisher"
print(first_member.club_name, first_member.member_name)
print(second_member.club_name, second_member.member_name)
