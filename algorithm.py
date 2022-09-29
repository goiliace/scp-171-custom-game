
from point import Point
from time import time


class Algorithm:
    def __init__(self, height, width, grid):
        self.height = height
        self.path = []
        self.width = width
        self.visited = set()
        self.grid = grid

    def find_path(self, node):
        while node.parent.parent != None:
            self.path.append(node)
            node = node.parent

    def reset(self):
        self.path = []
        self.visited = set()

    def getNeighbours(self, x, y):
        return [
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
        ]

    def getPath(self, start, goal):
        self.astar(start, goal)
        self.path.reverse()
        return [(p.x, p.y) for p in self.path]

    def gameTimeOne(self, start, goal, method):
        if method == "astar":
            start_time = time()
            self.astar(start, goal)
            return ["A*", time() - start_time]
        elif method == "greedy":
            start_time = time()
            self.greedy(start, goal)
            return ["Greedy", time() - start_time]
        elif method == "bfs":
            start_time = time()
            self.bfs(start, goal)
            return ["BFS", time() - start_time]

    def getTimeAll(self, start, goal):
        methods = ["astar", "greedy", "bfs"]
        return [self.gameTimeOne(start, goal, method) for method in methods]

    def bfs(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        queue = [S]  # tạo danh sách queue có 1 phần tử là điểm đầu vào

        self.visited.add((S.x, S.y))
        while queue:
            value = queue.pop(0)
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)

            neighbours = self.getNeighbours(value.x, value.y)
            for nx, ny in neighbours:
                if (
                    (nx, ny) not in self.visited
                    and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                    and (self.grid[nx][ny] != -1)
                ):
                    tmp = Point(nx, ny, par=value)
                    queue.append(tmp)
                    self.visited.add((tmp.x, tmp.y))

    def greedy(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        open = [S]
        dist = [S.heuristic_function(G)]
        self.visited.add((S.x, S.y))
        while open:
            idx = dist.index(min(dist))
            value = open.pop(idx)
            dist.pop(idx)
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)

            neighbours = self.getNeighbours(value.x, value.y)
            for nx, ny in neighbours:
                if (
                    (nx, ny) not in self.visited
                    and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                    and (self.grid[nx][ny] != -1)
                ):
                    tmp = Point(nx, ny, par=value)
                    open.append(tmp)
                    dist.append(tmp.heuristic_function(G))
                    self.visited.add((tmp.x, tmp.y))

    def astar(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        open = [S]
        distance = [S.heuristic_function(G)]
        self.visited.add((S.x, S.y))
        while open:
            idx = distance.index(min(distance))
            value = open.pop(idx)
            distance.pop(idx)
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)
            neighbours = self.getNeighbours(value.x, value.y)
            for nx, ny in neighbours:
                if (
                    (nx, ny) not in self.visited
                    and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                    and (self.grid[nx][ny] != -1)
                ):
                    tmp = Point(nx, ny, par=value, s=value.s + 1)
                    open.append(tmp)
                    distance.append(tmp.heuristic_function(G) + tmp.s)
                    self.visited.add((tmp.x, tmp.y))
