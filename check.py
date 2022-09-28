# graph = {'A': set(['B', 'C']),
#          'B': set(['A', 'D', 'E']),
#          'C': set(['A', 'F']),
#          'D': set(['B']),
#          'E': set(['B', 'F']),
#          'F': set(['C', 'E'])}

import numpy as np

graph = np.zeros((10, 10))


def dfs_paths(grid, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        (vertex, path) = stack.pop()
        print(vertex)
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


print(dfs_paths(graph, (0, 0), (9, 9)))  # ['A', 'B', 'E', 'F']


# class BFS:
# def __init__(self, height, width):
#     self.height = height
#     self.width = width

# def bfs(self, start, goal, grid, direction, x_h, y_h):
#     queue = deque()
#     queue.append((start,))
#     visited = set()
#     visited.add(start)
#     # print(grid)
#     while queue:
#         path = queue.popleft()
#         x, y = path[-1]
#         neighbours = [(x-1, y), (x, y+1),
#                       (x, y-1), (x+1, y)]
#         if (x, y) == goal:
#             # print(path)
#             return path
#         for nx, ny in neighbours:
#             if (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width) and ((nx, ny) not in visited) and (grid[nx][ny] != -1):
#                 # print("x: ", nx, "y: ", ny)
#                 new_path = list(path)
#                 new_path.append((nx, ny))
#                 queue.append(new_path)
#                 visited.add((nx, ny))
#     return []
