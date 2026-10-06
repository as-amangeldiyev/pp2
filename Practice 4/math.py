import math

# Convert degrees to radians.
degrees = float(input("Input degree: "))
print("Output radian:", degrees * math.pi / 180)

# Find the area of a trapezoid.
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
print("Trapezoid area:", (base1 + base2) * height / 2)

# Find the area of a regular polygon.
sides = int(input("Input number of sides: "))
side_length = float(input("Input the length of a side: "))
area = sides * side_length**2 / (4 * math.tan(math.pi / sides))
print("The area of the polygon is:", area)

# Find the area of a parallelogram.
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
print("Parallelogram area:", base * height)
