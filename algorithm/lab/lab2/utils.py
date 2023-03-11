import pygame
import math
import time

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (152, 251, 152)
BLUE = (0, 255, 0)
LIGHT_BLUE = (175, 238, 238)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

COLORS = {
    'closed': LIGHT_BLUE,
    'open': LIGHT_GREEN,
    'barrier': BLACK,
    # 'desert': YELLOW,
    # 'river': BLUE,
    'land': WHITE,
    'start': ORANGE,
    'end': RED
}

# LAND, RIVER, DESERT
EXTRA_COST = [0, 2, 4]


class Spot:
    def __init__(self, row, col, gap, ROWS, COLS, cost_idx=0):
        self.row = row
        self.col = col
        self.y = row * gap
        self.x = col * gap
        self.color = COLORS['land']
        self.cost_idx = cost_idx
        self.neighbors = []
        self.gap = gap
        self.total_rows = ROWS
        self.total_cols = COLS

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLORS['closed']

    def is_open(self):
        return self.color == COLORS['open']

    def is_barrier(self):
        return self.color == COLORS['barrier']

    def is_start(self):
        # return hasattr(self, 'start')
        return self.color == COLORS['start']

    def is_end(self):
        # return hasattr(self, 'end')
        return self.color == COLORS['end']

    def reset(self):
        self.color = COLORS['land']
        self.cost_idx = 0

    def reset_color(self):
        self.color = COLORS['land']

    def make_start(self):
        self.color = COLORS['start']

    def make_end(self):
        self.color = COLORS['end']

    def make_closed(self):
        self.color = COLORS['closed']

    def make_open(self):
        if not self.is_end(): self.color = COLORS['open']

    def make_barrier(self):
        self.color = COLORS['barrier']
        self.cost_idx = 0  # ?

    def make_path(self):
        # if not self.is_start(): self.color = YELLOW
        if not self.is_start() and not self.is_end(): self.color = YELLOW

    def draw(self, win):
        # 绘制矩形
        pygame.draw.rect(win, self.color, (self.x, self.y, self.gap, self.gap))
        if self.cost_idx:
            font = pygame.font.Font(None, self.gap)
            text = font.render(str(EXTRA_COST[self.cost_idx]), 1, GREY)
            textpos = text.get_rect()
            textpos.topleft = (self.x + self.gap // 4, self.y + self.gap // 4)
            win.blit(text, textpos)

    def update_neighbors(self, grid):
        self.neighbors = []
        di = [0, 0, -1, 1]
        dj = [1, -1, 0, 0]
        K = 4
        di = [0, 0, -1, -1, -1, 1, 1, 1]
        dj = [1, -1, -1, 0, 1, -1, 0, 1]
        K = 8
        for k in range(K):
            ni = self.row + di[k]
            nj = self.col + dj[k]
            if ni >= 0 and ni < self.total_rows \
                    and nj >= 0 and nj < self.total_cols \
                    and not grid[ni][nj].is_barrier():
                self.neighbors.append(grid[ni][nj])

    def __lt__(self, other):
        return self.row * self.total_cols + self.col


def make_grid(rows, cols, gap):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j, gap, rows, cols)
            grid[i].append(spot)
    return grid



def bye():
    pygame.quit()
    exit()


def reconstruct_path(came_from, current, draw):
    current.make_path()
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# 画网格线
def draw_grid(win, rows, cols, gap):
    width = cols * gap
    height = rows * gap
    for i in range(rows):
        # 横线
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # 竖线
        for j in range(cols):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, height))


def draw(win, grid, rows, cols, gap):
    # 背景填充为WHITE
    # 需要吗？
    win.fill(WHITE)

    # 每个格子填充对应颜色
    for row in grid:
        for spot in row:
            spot.draw(win)
    # 画网格线
    draw_grid(win, rows, cols, gap)
    pygame.display.update()


# x 水平向右
# y 水平向下
def get_clicked_pos(pos, gap):
    x, y = pos

    row = y // gap
    col = x // gap

    return row, col


def clear_trace(grid):
    for row in grid:
        for spot in row:
            if not spot.is_start() and not spot.is_end() and not spot.is_barrier():
                spot.reset_color()


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    d = min(abs(x1 - x2), abs(y1 - y2))
    return math.sqrt(2) * d + abs(x1 - x2) + abs(y1 - y2) - 2 * d

def load_map(filename):
    grid = []
    f = open(filename, 'r')
    [rows, cols, gap] = [int(s) for s in f.readline().split()]
    start = None
    end = None
    for i in range(rows):
        line = f.readline().split()
        grid.append([])
        for j in range(cols):
            grid[i].append(Spot(i, j, gap, rows, cols))
            cost_idx = 0
            if line[j][0] == 'S':
                grid[i][j].make_start()
                start = grid[i][j]
                cost_idx = int(line[j][1:])
            elif line[j][0] == 'T':
                grid[i][j].make_end()
                end = grid[i][j]
                cost_idx = int(line[j][1:])
            elif line[j] == '-1':
                grid[i][j].make_barrier()
            else:
                cost_idx = int(line[j])
            grid[i][j].cost_idx = cost_idx
    f.close()
    return grid, start, end, rows, cols, gap

def save_map(filename, grid):
    with open(filename, 'w') as f:
        rows = grid[0][0].total_rows
        cols = grid[0][0].total_cols
        gap = grid[0][0].gap
        f.write("{} {} {}\n".format(rows, cols, gap))
        for row in grid:
            for spot in row:
                if spot.is_barrier():
                    s = '-1'
                else:
                    if spot.is_start():
                        s = 'S'
                    elif spot.is_end():
                        s = 'T'
                    else:
                        s = ''
                    s += str(spot.cost_idx)
                f.write(s + ' ')
            f.write('\n')

def init_map(data_path,algo_name):
    ROWS = 20
    COLS = 40
    GAP = 34
    if len(data_path)>0:
        grid, start, end, ROWS, COLS, GAP = load_map(data_path)
    else:
        start = None
        end = None
        grid = make_grid(ROWS, COLS, GAP)

    # 设置窗口宽和高
    pygame.init()
    WIDTH = COLS * GAP
    HEIGHT = ROWS * GAP
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    if algo_name == 'astar':
        pygame.display.set_caption("A* Path Finding Algorithm")
    else:
        pygame.display.set_caption("Bidirectional A* Path Finding Algorithm")
    return WIN, ROWS, COLS, GAP,grid,start, end

def excute(algo,win, ROWS, COLS, GAP, grid, start = None, end = None):
    # 黄色格子代表沙漠，经过它的代价为 4 -- idx 2
    # 蓝色格子代表溪流，经过它的代价为 2 -- idx 1
    # 白色格子为普通地形，经过它的代价为 0 -- idx 0
    cost_idx = 0

    while True:
        draw(win, grid, ROWS, COLS, GAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bye()

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, GAP)
                print("pressed: ", row, col)
                spot = grid[row][col]
                if cost_idx:
                    if not spot.is_barrier(): spot.cost_idx = cost_idx
                    continue
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, GAP)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                print("key", event.key)
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    clear_trace(grid)
                    algo(lambda: draw(win, grid, ROWS, COLS, GAP), grid, start, end)
                elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                    idx = event.key - pygame.K_0
                    if idx < len(EXTRA_COST):
                        cost_idx = idx
                # save map
                elif event.key == pygame.K_s:
                    filename = time.strftime("%Y%m%d-%H%M%S.txt")
                    save_map(filename, grid)
                # new grid
                elif event.key == pygame.K_n:
                    start = None
                    end = None
                    grid = make_grid(ROWS, COLS, GAP)
                # clear trace
                elif event.key == pygame.K_c:
                    clear_trace(grid)
                # `q` to quit
                elif event.key == pygame.K_q:
                    bye()

    pygame.quit()