import numpy as np
from collections import deque

class BFS:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def bfs(self, start, goal, grid, direction, x_h, y_h):
        queue = deque()
        queue.append((start,))
        visited = set()
        visited.add(start)
        # print(grid)
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            neighbours = [(x-1, y), (x, y+1),
                          (x, y-1), (x+1, y)]
            if (x, y) == goal:
                return path
            for nx, ny in neighbours:
                if nx >= 0 and nx < self.height and ny >= 0 and ny < self.width and (nx, ny) not in visited and grid[ny][nx] == 0:
                    new_path = list(path)
                    new_path.append((nx, ny))
                    queue.append(new_path)
                    visited.add((nx, ny))
        return []
