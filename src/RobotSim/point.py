import math

def _epsilonEquals(a, b, epsilon = 0.001):
    return abs(a - b) < epsilon

class Pt:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __mul__(self, other):
        return Pt(self.x * float(other), self.y * float(other))

    def __rmul__(self, other):
        return Pt(self.x * float(other), self.y * float(other))

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return _epsilonEquals(self.x, other.x) and _epsilonEquals(self.y, other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Point only contains indices 0 and 1")

    def rotate(self, theta):
        return Pt(self.x * math.cos(theta) - self.y * math.sin(theta), self.y * math.cos(theta) + self.x * math.sin(theta))

    def asTuple(self):
        return (self.x, self.y)

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def serialize(self):
        return {"x": self.x, "y": self.y}
