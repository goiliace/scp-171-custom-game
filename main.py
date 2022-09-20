from time import time
import pygame
import numpy as np
from bfs import BFS
pygame.init()

screen = pygame.display.set_mode((600, 600))
shape = 60
pixel = 600//shape
grid = np.zeros((shape, shape))


class character_spritesheet:
    def __init__(self, image_spritesheet_path, cols, rows):
        # self.sheet = pygame.transform.scale2x(
        #     pygame.image.load(image_spritesheet_path))
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rows = rows
        self.cols = cols
        self.totalCell = self.rows * self.cols

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / self.cols
        h = self.cellHeight = self.rect.height / self.rows

        self.cells = list()
        for y in range(self.rows):
            for x in range(self.cols):
                self.cells.append([x * w, y * h, w, h])

    def draw_boss(self, surface, x, y, cellIndex, direction):
        if direction == "UP":
            cellIndex = cellIndex + 9
        if direction == "RIGHT":
            cellIndex = cellIndex + 6
        if direction == "DOWN":
            cellIndex = cellIndex
        if direction == "LEFT":
            cellIndex = cellIndex + 3
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

    def draw_human(self, surface, x, y, cellIndex, direction):
        if direction == "UP":
            cellIndex = cellIndex + 15
        if direction == "RIGHT":
            cellIndex = cellIndex + 25
        if direction == "DOWN":
            cellIndex = cellIndex + 5
        if direction == "LEFT":
            cellIndex = cellIndex + 35
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])


b = BFS(shape, shape)

boss = character_spritesheet("img/boss1.png", 3, 4)
human = character_spritesheet("img/human_1.png", 5, 8)
floor = pygame.transform.scale(
    pygame.image.load('img/floor10.png'), (600, 600))

key_5s = pygame.image.load('img/key_5s.png')
GAME_PLAY = True
clock = pygame.time.Clock()
x, y = 0, 0
x_h, y_h = 50, 50
x_old, y_old = 0, 0
direction = 'UP'
direction_boss = 'DOWN'
path = b.bfs((x, y), (170, 170), grid, direction, x_h, y_h)
L, D, R, U = 0, 0, 0, 0
L1, D1, R1, U1 = 0, 0, 0, 0
isFrozen5s = False
isFrozen2s = False
corr5s = (30, 20)
time5s = 0
time2s = 0
boss_detention = True
while GAME_PLAY:
    screen.fill((0, 0, 0))
    if corr5s:
        if corr5s[0] == x_h and corr5s[1] == y_h:
            isFrozen5s = True
            corr5s = None
        if isFrozen5s:
            time5s = time()
            isFrozen5s = False

    if ((time() - time2s) < 1):
        boss_detention = False
    elif ((time() - time5s) < 5):
        boss_detention = False
    else:
        boss_detention = True
    if path and boss_detention:
        x, y = path.pop(0)
        if (direction == 'RIGHT' and x <= x_h) or (direction == 'LEFT' and
                                                   x >= x_h) or (direction == 'UP' and y >= y_h) or (direction == 'DOWN' and y <= y_h):
            if x == x_old:
                if y < y_old:
                    direction_boss = 'UP'

                    L1 += 1
                    if L1 == 3:
                        L1 = 0
                else:
                    direction_boss = 'DOWN'

                    L1 += 1
                    if L1 == 3:
                        L1 = 0
            else:
                if x > x_old:
                    direction_boss = 'RIGHT'

                    L1 += 1
                    if L1 == 3:
                        L1 = 0
                else:
                    direction_boss = 'LEFT'

                    L1 += 1
                    if L1 == 3:
                        L1 = 0
            x_old, y_old = x, y
        else:
            time2s = time()
            path = []

    # screen.blit(human, (x_h*pixel, y_h*pixel))
    boss.draw_boss(screen, x*pixel, y*pixel, L1, direction_boss)
    human.draw_human(screen, x_h*pixel,
                     y_h*pixel, L, direction)
    if corr5s:
        screen.blit(key_5s, (corr5s[0]*pixel, corr5s[1]*pixel))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_PLAY = False
        if event.type == pygame.KEYDOWN:
            L += 1
            if L == 5:
                L = 0
            if event.key == pygame.K_LEFT:

                if direction == 'LEFT':
                    x_h -= 1

                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)
                else:
                    direction = 'LEFT'
                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)

            if event.key == pygame.K_RIGHT:
                if direction == 'RIGHT':

                    x_h += 1
                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)

                else:
                    direction = 'RIGHT'

                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)

            if event.key == pygame.K_UP:
                if direction == 'UP':
                    direction = 'UP'

                    y_h -= 1
                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)

                else:
                    direction = 'UP'
                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)

            if event.key == pygame.K_DOWN:
                if direction == 'DOWN':
                    y_h += 1
                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)

                else:
                    direction = 'DOWN'
                    path = b.bfs((x_old, y_old), (x_h, y_h),
                                 grid, direction, x_h, y_h)

    pygame.display.update()
    clock.tick(60)
