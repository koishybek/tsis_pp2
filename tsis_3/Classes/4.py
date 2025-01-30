class Point:
    def setCoords(self, x, y):
        self.x = x
        self.y = y
    def show(self):
        print(self.x, self.y)
    def move(self, x, y):
        self.x = x
        print()
        self.y = y
    def dist(self, other):
        import math
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
