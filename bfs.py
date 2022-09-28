from cgitb import reset
import numpy as np
from collections import deque


class Point():
    # hàm khởi tạo gồm tọa độ x, y và con trỏ par
    def __init__(self, x: int, y: int, l=None, s=None, par=None):
        self.x = x
        self.y = y
        self.l = l  # độ sâu của node dùng cho dfs_limited, dfs_deepen
        self.s = s  # quãng đường đã đi được dùng trong A_star
        self.par = par


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

    def dfs(self, start: tuple, goal: tuple, grid: list):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        stack = [S]
        while stack:
            # lấy giá trị cuối cùng trong danh sách, đồng thời xóa đối tượng đó khỏi danh sách stack
            value = stack.pop(-1)
            if value.x == G.x and value.y == G.y:
                return self.path(value)
            neighbours = [(value.x-1, value.y), (value.x, value.y+1),
                          (value.x, value.y-1), (value.x+1, value.y)]
            for nx, ny in neighbours:
                if (nx, ny) not in visited and\
                        (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width) and (grid[nx][ny] != -1):
                    tmp = Point(nx, ny, par=value)
                    queue.append(tmp)
                    visited.add((tmp.x, tmp.y))
            for i in range(4):
                new_x = value.x + self.col[i]
                new_y = value.y + self.row[i]
                # kiểm tra vị trí quái vật
                if self.checkMonsters(new_x, new_y):
                    tmp = Point(new_x, new_y)
                    if self.checkVisited(new_x, new_y):
                        tmp.par = value
                        # thêm vị trí mới vào vào cuối danh sách stack
                        stack.append(tmp)
                        
                        
    def dfs(self, start, goal, grid):
        stack = [(start, [start])]
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            # print(vertex)
            (x, y) = vertex
            # x,y = path[-1]
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                neighbours = [(x-1, y), (x, y+1),
                              (x, y-1), (x+1, y)]
                for nx, ny in neighbours:
                    # and (graph[nx][ny] != -1):
                    if (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width) and ((nx, ny) not in visited) and (grid[nx][ny] != -1):
                        stack.append(((nx, ny), path + [(nx, ny)]))
        return []
