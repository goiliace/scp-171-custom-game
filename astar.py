from math import sqrt
from point import Point

class Astar:
    def __init__(self, height,width):
        self.height = height
        self.width = width
        self.visited = list()
        self.final_path = list()
    
    def path(self, p):
        self.final_path.append(p)  # thêm đối tượng vào danh sách kết quả
        if p.par != None:  # kiểm tra nếu địa chỉ đối tượng tiếp theo chưa None thì tiếp tục đệ quy
            return self.path(p.par)
    
    def check_visited(self, other):
        for i in self.visited:
            if i == other:
                return True
        return False
    
    def astar(self, grid, S: Point, G: Point):
        open = [S]
        distance = [S.heuristic_function(G)]
        while len(open) != 0:
            idx = distance.index(min(distance))
            P = open.pop(idx)
            distance.pop(idx)
            x, y = P.get_XY()
            P1, P2, P3, P4 = Point(x-1, y, s = P.s+1), Point(x, y+1, s = P.s+1), Point(x, y-1, s = P.s+1), Point(x+1, y, s = P.s+1)
            neighbours = [P1, P2, P3, P4]
            for i in range(4):
                if neighbours[i] == G:
                    self.path(Point)
                    return self.final_path
                if not(neighbours[i].x >= 0 and neighbours[i].x < self.height) or not(neighbours[i].y >= 0 and neighbours[i].y < self.width) or self.check_visited(neighbours[i]) or (grid[neighbours[i].x][neighbours[i].y] == -1):
                    self.visited.add(i)
                    continue
                neighbours[i].set_par(P)
                distance.append(neighbours[i].heuristic_function(G) + neighbours[i].s)
                
                
            