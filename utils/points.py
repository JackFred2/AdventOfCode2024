import math


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if type(other) == Point:
            return Point(self.x + other.x, self.y + other.y)
        elif type(other) == tuple:
            return Point(self.x + other[0], self.y + other[1])
        else:
            raise ValueError("Added point and not a point/tuple", type(other))

    def __sub__(self, other):
        if type(other) == Point:
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise ValueError("Added point and not a point")

    def __eq__(self, other):
        return type(other) == Point and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def neighbours(self):
        return [
            self + Point(1, 0),
            self + Point(0, 1),
            self + Point(-1, 0),
            self + Point(0, -1),
        ]

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def manhattan_distance(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

