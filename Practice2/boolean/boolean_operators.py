age = 20
has_ticket = True
is_member = False

print("Can enter:", age >= 18 and has_ticket)
print("Gets a discount:", is_member or age < 12)
print("Not a member:", not is_member)
