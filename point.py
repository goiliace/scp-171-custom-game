import numpy as np


class Point:
    def __init__(self, x, y, par=None, s=0) -> None:
        self.x = x
        self.y = y
        self.s = s
        self.parent = par

    def get_XY(self):
        return self.x, self.y

    def get_par(self):
        return self.parent

    def set_par(self, new_par):
        self.parent = new_par

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        return False if other == None else (self.x == other.x and self.y == other.y)

    # manhattan_distance
    def heuristic_function(self, other: object):
        # return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        # Calculating the distance between two points.
        return abs(self.x - other.x) + abs(self.y - other.y)
