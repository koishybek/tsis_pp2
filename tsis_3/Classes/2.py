class Shape:
    def area(self):
        return 0

class Square(Shape):
    length = 5
    
    def area(self):
        return self.length * self.length

square = Square()
print(square.area())
