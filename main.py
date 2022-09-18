
import pygame
import numpy as np
from collections import deque
pygame.init()

screen = pygame.display.set_mode((600, 600))
shape = 100
pixel = 600/shape
grid = np.zeros((shape, shape))


class BFS:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def bfs(self, start, goal, grid):
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
            if (x, y) == (goal[0], goal[1]):
                return path
            for nx, ny in neighbours:
                if nx >= 0 and nx < self.height and ny >= 0 and ny < self.width and (nx, ny) not in visited and grid[nx][ny] == 0:
                    new_path = list(path)
                    new_path.append((nx, ny))
                    queue.append(new_path)
                    visited.add((nx, ny))
        return []


b = BFS(shape, shape)
boss = pygame.image.load('img/boss.png')
floor = pygame.transform.scale(
    pygame.image.load('img/floor10.png'), (600, 600))
human = pygame.image.load('img/human.png')





GAME_PLAY = True
clock = pygame.time.Clock()
x, y = 0, 0
x_h, y_h = 7, 7
x_old, y_old = 0, 0
direction = 'U'
path = b.bfs((x, y), (70, 70), grid)
while GAME_PLAY:
    screen.blit(floor, (0, 0))
    screen.blit(boss, (x_old*pixel, y_old*pixel))

    if len(path) > 0:
        x, y = path.pop(1)
        if direction == 'R' and x < x_h*10 or direction == 'L' and \
                x > x_h*10 or direction == 'U' and y > y_h*10 or direction == 'D' and y+1 < y_h*10:
            screen.blit(floor, (0, 0))

            screen.blit(boss, (x*pixel, y*pixel))
            screen.blit(human, (x_h*pixel*10, y_h*pixel*10))
            x_old, y_old = x, y
        else:
            path = []
    screen.blit(human, (x_h*pixel*10, y_h*pixel*10))
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            GAME_PLAY = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                path = b.bfs((x_old, y_old), (x_h*10, y_h*10), grid)
                x_h -= 1
                direction = 'L'
            if event.key == pygame.K_RIGHT:
                path = b.bfs((x_old, y_old), (x_h*10, y_h*10), grid)
                x_h += 1
                direction = 'R'
            if event.key == pygame.K_UP:
                path = b.bfs((x_old, y_old), (x_h*10, y_h*10), grid)
                y_h -= 1
                direction = 'U'
            if event.key == pygame.K_DOWN:
                path = b.bfs((x_old, y_old), (x_h*10, y_h*10), grid)
                y_h += 1
                direction = 'D'

    pygame.display.update()
    clock.tick(60)
