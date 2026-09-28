class Circle():
    def __init__(self,radius):
        self.radius = radius
    def findarea(self):
        self.area = 3.14*(self.radius**2)    
        print("Area of the circle is", self.area)
circle = Circle(5)

circle.findarea()