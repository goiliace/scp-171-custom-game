from math import sqrt
class Point():
    def __init__(self, x, y, par = None, s = None) -> None:
        self.x = x
        self.y = y
        self.s = s
        self.par = par

    def get_XY(self):
        return self.x, self.y
    
    def get_par(self):
        return self.par
    
    def set_par(self, new_par):
        self.par = new_par
    
    def __repr__(self):
       return f"({self.x}, {self.y})"
    
    def __eq__(self, other: object) -> bool:
        return False if other == None else (self.x == other.x and self.y == other.y)

    def heuristic_function(self, other: object):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


