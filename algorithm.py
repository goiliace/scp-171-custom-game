import numpy as np  # thư viện xử lí ma trận mạnh
import pandas as pd  # thư viện trực quan với dữ liệu có cấu trúc
from time import time  # lấy 1 hàm đánh dấu thời gian

# tạo class để lưu cấu trúc dữ liệu tọa độ


class Point():
    # hàm khởi tạo gồm tọa độ x, y và con trỏ par
    def __init__(self, x: int, y: int, l=None, s=None, par=None):
        self.x = x
        self.y = y
        self.l = l  # độ sâu của node dùng cho dfs_limited, dfs_deepen
        self.s = s  # quãng đường đã đi được dùng trong A_star
        self.par = par

    # hàm tính khoảng cách giữa 2 tọa độ
    def distance(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def kc(self, other):
        print(f'({self.x}, {self.y}) - {self.s}, {self.distance(other)}')

# ----------------------------------------------------------------
# tạo class để làm các thuật toán


class Search():
    # tạo 2 thuộc tính thể hiện vị trí di chuyển
    row = [1, 0, -1, 0]  # y
    col = [0, 1, 0, -1]  # x

    ''' hàm khởi tạo gồm các đầu vào:
            - w (int - kiểu số nguyên): độ rộng khung màn hình chính của game
            - h (int - kiểu số nguyên): độ cao khung màn hình chính của game
            - monster (list - kiểu danh sách): danh sách các tọa độ vật cản/quái vật
    và biến - res (list - kiểu danh sách) để lưu tọa độ đường đi khi chạy thuật toán
            - matrix_visit (array - kiểu danh sách 1 thuộc tính) là ma trận đánh dấu những tọa độ đã đi qua
    '''

    def __init__(self, w, h, monster):
        self.w = w
        self.h = h
        self.monster = monster
        self.res = []
        self.matrix_visit = np.array([False]*(w*h)).reshape(w, h)

    # hàm này dùng để làm trống biến lưu trữ mỗi lần tìm kiếm
    def reset(self):
        self.res = []
        self.matrix_visit = np.array(
            [False]*(self.w*self.h)).reshape(self.w, self.h)

    # hàm này dùng để kiểm tra tọa độ hiện tại có thỏa mãn các điều kiện hay không
    def checkVisited(self, x, y):
        # nếu tọa độ ở ngoài biên (khung game) hoặc là tọa độ của vật cản (quái vật) thì trả về False
        if x < 0 or x > self.w-1 or y < 0 or y > self.h-1:
            return False
        # nếu tọa độ là chỗ đã đi qua rồi (vị trí trên ma trận kiểm tra có giá trị True) thì trả về False
        if self.matrix_visit[x][y]:
            return False
        # không khỏa mãn các điều kiện trên thì trả về True
        return True

    def checkMonsters(self, x, y):
        if (x, y) in self.monster:
            return False
        return True

    # hàm này dùng để truy xuất ngược lại các nút đã đi qua từ điểm bắt đầu đến kết thúc thông qua giá trị của par
    # đầu vào là 1 cấu trúc Point
    def path(self, p):
        self.res.append(p)  # thêm đối tượng vào danh sách kết quả
        if p.par != None:  # kiểm tra nếu địa chỉ đối tượng tiếp theo chưa None thì tiếp tục đệ quy
            return self.path(p.par)
        else:
            return

    # thuật toán BFS (Breadth-First Search -- Tìm kiếm theo chiều rộng)
    # đầu vào là 2 tọa độ bắt đầu và kết thúc có kiểu tuple
    def bfs(self, start: tuple, goal: tuple):
        self.reset()  # làm mới biến lưu trữ kết quả và ma trận kiểm tra
        # tạo 2 đối tượng bắt đầu và kết thúc
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        queue = [S]  # tạo danh sách queue có 1 phần tử là điểm đầu vào

        # cho vòng lặp chạy đến khi nào ko còn đối tượng trong danh sách queue nữa
        while len(queue) > 0:
            # lấy giá trị đầu tiên trong danh sách, đồng thời xóa đối tượng đó khỏi danh sách queue
            value = queue.pop(0)
            # đánh dấu vị trí này vào ma trận kiểm tra
            self.matrix_visit[value.x, value.y] = True
            # kiểm tra tọa độ đang xử lí có phải điểm cần đến hay không
            if value.x == G.x and value.y == G.y:
                # nếu đúng thì chuyển sang hàm path để truy xuất ra kết quả đường đi (output bài toán)
                return self.path(value)
            # nếu không phải tọa độ đích đến thì xét các tọa độ tiếp theo có thể đi
            # ở đây mặc định nhân vật chỉ có thể đi ngang và dọc nên dùng for chạy 4 lần lặp: trên - trái - dưới - phải (chiều kim đồng hồ)
            for new_x, new_y in zip(self.col, self.row):
                # tạo 2 biến để lưu trữ tọa độ mới
                # kiểm tra vị trí quái vật
                if self.checkMonsters(new_x, new_y):
                    # tạo biến lưu trữ tạm thời điểm mới đó
                    tmp = Point(new_x, new_y)
                    # kiểm tra ma trận thăm, nếu trả về True thì có nghĩa ko bị vi phạm ràng buộc và tiếp tục công việc dưới
                    if self.checkVisited(new_x, new_y):
                        tmp.par = value  # biến con trỏ trỏ đến địa chỉ của vị trí trước đó
                        # thêm vị trí mới vào vào cuối danh sách queue
                        queue.append(tmp)

    # thuật toán DFS (Depth-First Search -- Tìm kiếm theo chiều sâu)
    # đầu vào tương tự như BFS
    # 1 vài thao tác tương tự như trên nên mình không comment thêm nữa

    def dfs(self, start: tuple, goal: tuple):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        stack = [S]
        while len(stack) > 0:
            # lấy giá trị cuối cùng trong danh sách, đồng thời xóa đối tượng đó khỏi danh sách stack
            value = stack.pop(-1)
            self.matrix_visit[value.x, value.y] = True
            if value.x == G.x and value.y == G.y:
                return self.path(value)
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

    # thuật toán tìm kiếm chiều sau có giới hạn
    # đầu vào tương tự, có biến l=1 tức là nếu không truyền giá trị cho tham số l thì l tự động được đặt là 1
    def dfs_limited(self, start, goal, l=1):
        self.reset()
        deep = 0
        S = Point(start[0], start[1], deep)
        G = Point(goal[0], goal[1])
        stack = [S]
        while len(stack) > 0:
            value = stack.pop(-1)
            self.matrix_visit[value.x, value.y] = True
            if value.x == G.x and value.y == G.y:
                return self.path(value)
            deep = value.l + 1  # chiều sâu bằng chiều sâu nút cha tăng 1
            for i in range(4):
                new_x = value.x + self.col[i]
                new_y = value.y + self.row[i]
                if self.checkMonsters(new_x, new_y) and self.checkVisited(new_x, new_y):
                    tmp = Point(new_x, new_y, deep)
                    tmp.l = deep
                    if deep <= l:
                        tmp.par = value
                        stack.append(tmp)
        return l+1  # nếu không tìm thấy thì trả về chiều sâu +1

    # thuật toán tìm kiếm sâu dần
    # mình dùng vòng lặp vô tận để tìm kiếm thông qua hàm thuật toán có giới hạn
    def dfs_deepen(self, start, goal):
        self.reset()
        test = 1
        while True:
            test = self.dfs_limited(start, goal, test)
            if len(self.res) != 0:
                return

    # thuật toán greedy -- thuật toán tham ăn
    # ý tưởng: tìm vị trí gần nhất với vị trí đích. "Độ gần" được ước tính bằng khoảng cách giữa 2 tọa độ
    def greedy(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        queue = [S]
        dist = [S.distance(G)]
        while True:
            idx = dist.index(min(dist))
            value = queue.pop(idx)
            dist.pop(idx)
            self.matrix_visit[value.x, value.y] = True
            if value.x == G.x and value.y == G.y:
                return self.path(value)
            for i in range(4):
                new_x = value.x + self.col[i]
                new_y = value.y + self.row[i]
                if self.checkMonsters(new_x, new_y):
                    tmp = Point(new_x, new_y)
                    if self.checkVisited(new_x, new_y):
                        tmp.par = value
                        queue.append(tmp)
                        dist.append(tmp.distance(G))

    def A_star(self, start, goal):
        self.reset()
        S = Point(start[0], start[1], s=0)
        G = Point(goal[0], goal[1])
        queue = [S]
        dist_sum = [S.distance(G)]
        while True:
            idx = dist_sum.index(min(dist_sum))
            value = queue.pop(idx)
            dist_sum.pop(idx)
            self.matrix_visit[value.x, value.y] = True
            # value.kc(G)
            # print([(p.x, p.y) for p in queue])
            # print(dist_sum)
            if value.x == G.x and value.y == G.y:
                return self.path(value)
            for i in range(4):
                new_x = value.x + self.col[i]
                new_y = value.y + self.row[i]
                if self.checkMonsters(new_x, new_y):
                    tmp = Point(new_x, new_y, s=value.s + 1)
                    if self.checkVisited(new_x, new_y):
                        tmp.par = value
                        queue.append(tmp)
                        dist_sum.append(tmp.distance(G)+tmp.s)
    # hàm này dùng để kiểm tra xem có tìm được đường đến đích hay không

    def status(self):
        if len(self.res) == 0:
            print('Not found!')
        else:
            print('Success!')

    # hàm này dùng để chạy 1 thuật toán với đầu vào là 2 tọa độ bắt đầu và kết thúc với loại thuật toán
    # trả về danh sách chứa: tên thuật toán dùng (str) - thời gian chạy thuật toán (float) - danh sách các tọa dộ để đến đích (list)
    def runOne(self, s: tuple, g: tuple, option: str):
        match option.upper():
            case 'BFS':
                start_time = time()
                self.bfs(s, g)
                end_time = time()
                return ['BFS', (end_time-start_time)*1000, [(p.x, p.y) for p in self.res][::-1]]
            case 'DFS':
                start_time = time()
                self.dfs(s, g)
                end_time = time()
                return ['DFS', (end_time-start_time)*1000, [(p.x, p.y) for p in self.res][::-1]]
            case 'IDS':
                start_time = time()
                self.dfs_deepen(s, g)
                end_time = time()
                return ['IDS', (end_time-start_time)*1000, [(p.x, p.y) for p in self.res][::-1]]
            case 'GREEDY':
                start_time = time()
                self.greedy(s, g)
                end_time = time()
                return ['GREEDY', (end_time-start_time)*1000, [(p.x, p.y) for p in self.res][::-1]]
            case 'A_STAR':
                start_time = time()
                self.A_star(s, g)
                end_time = time()
                return ['A*', (end_time-start_time)*1000, [(p.x, p.y) for p in self.res][::-1]]

    # hàm này dùng để chạy tất cả các thuật toán
    def runAll(self, s: tuple, g: tuple):
        opt = ['bfs', 'dfs', 'ids', 'greedy', 'a_star']
        return [self.runOne(s, g, x) for x in opt]

    # hàm này dùng để xem thống kê thông tin của các thuật toán
    def viewInfo(self, s: tuple, g: tuple):
        d = self.runAll(s, g)
        name = [d[i][0] for i in range(5)]
        time = [d[i][1] for i in range(5)]
        number_of_steps = [len(d[i][2]) for i in range(5)]
        df = pd.DataFrame({'Name': name, 'Time (ms)': time,
                          'Number of Steps': number_of_steps})
        print(df)
