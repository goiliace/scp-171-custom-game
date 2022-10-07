import pickle
from time import time
import pygame
import numpy as np
from algorithm import Algorithm

pygame.init()
height = 960
screen = pygame.display.set_mode((height, height))
shape = 120
pixel = height // shape
grid = np.genfromtxt("map/map3.csv", delimiter=",")
print(grid.shape)


class CharacterSpriteSheet:
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
            cellIndex = cellIndex + 5
        if direction == "RIGHT":
            cellIndex = cellIndex + 10
        if direction == "DOWN":
            pass
        if direction == "LEFT":
            cellIndex = cellIndex + 15
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


b = Algorithm(shape, shape, grid)

boss = CharacterSpriteSheet("img/boss1.png", 3, 4)
human = CharacterSpriteSheet("img/human.png", 5, 4)
floor = pygame.transform.scale(pygame.image.load("img/floor10.png"), (height, height))

key_2s = pygame.image.load("img/key_2.png")
key_2s = pygame.transform.scale(key_2s, (30, 30))
key_3s = pygame.image.load("img/key_3.png")
key_3s = pygame.transform.scale(key_3s, (30, 30))
key_1s = pygame.image.load("img/key_1.png")
key_1s = pygame.transform.scale(key_1s, (30, 30))
clock_5s = pygame.image.load("img/clock.png")
clock_5s = pygame.transform.scale(
    clock_5s, (clock_5s.get_width() // 5, clock_5s.get_height() // 5)
)
game_over = pygame.image.load("img/game_over.jpg")
game_over = pygame.transform.scale(game_over, (height, height))
dooropen = pygame.image.load("img/dooropen.png")
buff = pygame.image.load("img/buff.png")
buff = pygame.transform.scale(buff, (buff.get_width() // 5, buff.get_height() // 5))
shield = pygame.image.load("img/shield.png")
shield = pygame.transform.scale(
    shield, (shield.get_width() // 5, shield.get_height() // 5)
)
GAME_PLAY = True
clock = pygame.time.Clock()
x, y = 53, 3
x_h, y_h = 8, 113  # human
x_old, y_old = x, y
direction = "DOWN"
direction_boss = "RIGHT"
path = b.bfs((x, y), (170, 170))
L, D, R, U = 0, 0, 0, 0
L1, D1, R1, U1 = 0, 0, 0, 0
isFrozen5s = False
isFrozen2s = False
corr5s = (72, 108)
corr3s = (30, 90)
corr2s = (100, 25)
key_1_point = (108, 110)
key_2_point = (55, 39)
key_3_point = (101, 9)
buff_point = (25, 115)
buff1_point = (82, 24)
shield_point = (4, 68)
coin1 = pygame.image.load("img/coin1.png")
coin2 = pygame.image.load("img/coin2.png")
coin3 = pygame.image.load("img/coin3.png")
coin4 = pygame.image.load("img/coin4.png")
coin5 = pygame.image.load("img/coin5.png")
coin6 = pygame.image.load("img/coin6.png")
coin7 = pygame.image.load("img/coin7.png")
coin8 = pygame.image.load("img/coin8.png")
coin9 = pygame.image.load("img/coin9.png")
coin10 = pygame.image.load("img/coin10.png")

time5s = 0
time2s = 0
countKeyOpenDoor = 0
boss_detention = True
map = pygame.image.load("map/map3.png")
map = pygame.transform.scale(map, (height, height))
pos_coin = [(20, 19)]


def checkKey(x, y, key_point, countKeyOpenDoor):
    if key_point:
        if distance(key_point[0], key_point[1], x, y) < 5:
            key_point = None
            countKeyOpenDoor += 1
    return key_point, countKeyOpenDoor


def drawCoin():
    for i, pos in enumerate(pos_coin):
        if i % 10 == 0:
            screen.blit(coin1, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 1:
            screen.blit(coin2, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 2:
            screen.blit(coin3, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 3:
            screen.blit(coin4, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 4:
            screen.blit(coin5, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 5:
            screen.blit(coin6, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 6:
            screen.blit(coin7, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 7:
            screen.blit(coin8, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 8:
            screen.blit(coin9, (pos[0] * pixel, pos[1] * pixel))
        if i % 10 == 9:
            screen.blit(coin10, (pos[0] * pixel, pos[1] * pixel))


isPress = True
timePress = 0
speed = 0.01
timeBuff = 0
timeShield = 0
timebfs = 0
timedfs = 0
gameTimeList = []
while GAME_PLAY:

    screen.fill((0, 0, 0))
    screen.blit(map, (0, 0))
    drawCoin()
    if corr5s:
        if distance(corr5s[0], corr5s[1], x_h, y_h) < 2:
            isFrozen5s = True
            corr5s = None
        if isFrozen5s:
            time5s = time()
            isFrozen5s = False
    key_1_point, countKeyOpenDoor = checkKey(x_h, y_h, key_1_point, countKeyOpenDoor)
    key_2_point, countKeyOpenDoor = checkKey(x_h, y_h, key_2_point, countKeyOpenDoor)
    key_3_point, countKeyOpenDoor = checkKey(x_h, y_h, key_3_point, countKeyOpenDoor)
    if buff_point:
        if distance(buff_point[0], buff_point[1], x_h, y_h) < 3:
            buff_point = None
            speed = 0.005
            timeBuff = time()
    if buff1_point:
        if distance(buff1_point[0], buff1_point[1], x_h, y_h) < 4:
            buff1_point = None
            speed = 0.005
            timeBuff = time()
    if time() - timeBuff > 5:
        speed = 0.05
    if countKeyOpenDoor == 3:
        screen.blit(dooropen, (18, 8))
    if (time() - time2s) < 2:
        boss_detention = False
    elif (time() - time5s) < 5:
        boss_detention = False
    else:
        boss_detention = True
    if shield_point:
        if distance(shield_point[0], shield_point[1], x_h, y_h) < 2:
            shield_point = None
            isShield = True
            timeShield = time()
    if time() - timeShield > 10:
        isShield = False

    if path and boss_detention:
        x, y = path.pop(0)
        if (
            (direction == "RIGHT" and y <= y_h)
            or (direction == "LEFT" and y >= y_h)
            or (direction == "UP" and x >= x_h)
            or (direction == "DOWN" and x <= x_h)
        ):
            if x == x_old:
                if y < y_old:
                    direction_boss = "UP"
                    L1 += 1
                    if L1 == 3:
                        L1 = 0
                else:
                    direction_boss = "DOWN"
                    L1 += 1
                    if L1 == 3:
                        L1 = 0
            else:
                if x > x_old:
                    direction_boss = "RIGHT"

                    L1 += 1
                    if L1 == 3:
                        L1 = 0
                else:
                    direction_boss = "LEFT"

                    L1 += 1
                    if L1 == 3:
                        L1 = 0
            x_old, y_old = x, y
        else:
            time2s = time()
            path = []

    # screen.blit(human, (x_h*pixel, y_h*pixel))

    boss.draw_boss(screen, y * pixel - 10, x * pixel - 28, L1, direction_boss)
    # Drawing a red rectangle at the position of the boss.
    # pygame.draw.rect(screen, (255, 0, 0), (y * pixel, x * pixel, pixel, pixel))

    human.draw_human(screen, y_h * pixel - 10, x_h * pixel - 32, L, direction)
    if corr5s:
        screen.blit(clock_5s, (corr5s[1] * pixel, corr5s[0] * pixel))
    if key_1_point:
        screen.blit(key_2s, (key_1_point[1] * pixel, key_1_point[0] * pixel))
    if key_2_point:
        screen.blit(key_3s, (key_2_point[1] * pixel, key_2_point[0] * pixel))
    if key_3_point:
        screen.blit(key_1s, (key_3_point[1] * pixel, key_3_point[0] * pixel))
    if buff_point:
        screen.blit(buff, (buff_point[1] * pixel, buff_point[0] * pixel))
    if shield_point:
        screen.blit(shield, (shield_point[1] * pixel, shield_point[0] * pixel))
    if buff1_point:
        screen.blit(buff, (buff1_point[1] * pixel, buff1_point[0] * pixel))
    if isShield:
        screen.blit(shield, (y_h * pixel - 5, x_h * pixel - 13))
        if x_old == x_h and y_h == y_old:
            x_old, y_old = np.random.randint(0, 120), np.random.randint(0, 120)

            while grid[x_old][y_old] == -1:
                x_old, y_old = np.random.randint(0, 120), np.random.randint(0, 120)
            isShield = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_PLAY = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and isPress:
        L += 1
        if L == 5:
            L = 0

        if direction == "LEFT":
            if grid[x_h][y_h - 1] != -1:
                y_h -= 1
        else:
            direction = "LEFT"

    if keys[pygame.K_RIGHT] and isPress:
        L += 1
        if L == 5:
            L = 0
        if direction == "RIGHT":
            if grid[x_h][y_h + 1] != -1:
                y_h += 1

        else:
            direction = "RIGHT"

    if keys[pygame.K_UP] and isPress:
        L += 1
        if L == 5:
            L = 0
        if direction == "UP":
            if grid[x_h - 1][y_h] != -1:
                x_h -= 1

        else:
            direction = "UP"

    if keys[pygame.K_DOWN] and isPress:
        L += 1
        if L == 5:
            L = 0
        if direction == "DOWN":
            if grid[x_h + 1][y_h] != -1:
                x_h += 1

        else:
            direction = "DOWN"

    if (
        keys[pygame.K_LEFT]
        or keys[pygame.K_RIGHT]
        or keys[pygame.K_UP]
        or keys[pygame.K_DOWN]
    ) and isPress:
        isPress = False
        timebfs = time()
        gameTimeList.append(b.getTimeAll((x_old, y_old), (x_h, y_h)))
        path = b.getPath((x_old, y_old), (x_h, y_h))
        timePress = time()
    if time() - timePress > speed:
        isPress = True
    if x_old == x_h and y_old == y_h and not isShield:
        screen.blit(game_over, (0, 0))
    pygame.display.update()
    clock.tick(60)
# print(gameTimeList)
pickle.dump(gameTimeList, open("timeAl.dat", "wb"))
