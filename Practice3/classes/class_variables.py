"""Examples of the difference between class and instance variables."""


class ClubMember:
    club_name = "Python Club"

    def __init__(self, member_name):
        self.member_name = member_name


first_member = ClubMember("Ali")
second_member = ClubMember("Sara")
first_member.member_name = "Alisher"
print(first_member.club_name, first_member.member_name)
print(second_member.club_name, second_member.member_name)
