class Shape:
    def area(self):
        return 0

class Square(Shape):
    length = 5
    
    def area(self):
        return self.length * self.length

class Rectangle(Shape):
    length = 4
    width = 6
    
    def area(self):
        return self.length * self.width

square = Square()
print(square.area())

rectangle = Rectangle()
print(rectangle.area())
