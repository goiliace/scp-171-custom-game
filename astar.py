from queue import PriorityQueue
from math import hypot

class ASTAR:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.visited = set()
        self.final_path = []
        
    def astar(self, start: tuple, goal:tuple):
        x_end, y_end = goal
        queue = [start]
        self.visited.add(start)
        while len(queue) != 0:
            x, y = queue[0][0], queue[0][1]
            if (x, y) == goal:
                return self.final_path
            neighbours = [(x-1, y), (x, y+1),
                          (x, y-1), (x+1, y)]
            path = []
            for i, j in neighbours:
                if (i, j) in self.visited:
                    continue
                dist = get_distance(i, j, x_end, y_end)
                path.append((dist, i, j))
                self.visited.append((i, j))
            path = min(path)
            self.final_path.append((path[1], path[2]))
            
def get_distance(x_start, y_start, x_end, y_end):
        return hypot((x_start - x_end), (y_start - y_end))

