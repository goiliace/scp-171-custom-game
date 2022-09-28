from cgitb import reset
import numpy as np
from collections import deque
from point import Point




class BFS:
    def __init__(self, height, width):
        self.height = height
        self.res = []
        self.width = width
        

    def path(self, p):
        self.res.append(p)  # thêm đối tượng vào danh sách kết quả
        if p.par != None:  # kiểm tra nếu địa chỉ đối tượng tiếp theo chưa None thì tiếp tục đệ quy
            return self.path(p.par)
        

    def reset(self):
        self.res = []

    def bfs(self, start, goal, grid):
        reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        queue = [S]  # tạo danh sách queue có 1 phần tử là điểm đầu vào
        visited = set()                                                                                                                                                                                                         
        visited.add((S.x, S.y))
        while queue:
            value = queue.pop(0)
            if value.x == G.x and value.y == G.y:
                self.path(value)
                return [(p.x, p.y) for p in self.res][::-1]
            neighbours = [(value.x-1, value.y), (value.x, value.y+1),
                          (value.x, value.y-1), (value.x+1, value.y)]
            for nx, ny in neighbours:
                if (nx,ny) not in visited and\
                    (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width) and (grid[nx][ny] != -1):
                    tmp = Point(nx, ny, par=value)
                    queue.append(tmp)
                    visited.add((tmp.x, tmp.y))