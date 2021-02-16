import math
import time

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def length(self):
        return math.sqrt(
            (self.x ** 2) +
            (self.y ** 2) +
            (self.z ** 2)
        )
    
    def normalize(self):
        length = self.length()
        return Vector(
            self.x / length,
            self.y / length,
            self.z / length,
        )

    def reverse(self):
        return Vector(
            self.x * -1,
            self.y * -1,
            self.z * -1
        )

    @staticmethod
    def vector_from_points(point1, point2):
        return Vector(
            (point2.x - point1.x),
            (point2.y - point1.y),
            (point2.z - point1.z)
        )

    def __str__(self):
        return "({}, {}, {})".format(
            self.x,
            self.y,
            self.z
        )

    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        other = other.reverse()
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Vector(
                self.x * other,
                self.y * other,
                self.z * other
            )
        elif type(other) == Vector:
            return Vector(0, 0, 0)
