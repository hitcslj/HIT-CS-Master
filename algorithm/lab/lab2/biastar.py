import sys
import time
from utils import *
import heapq

def biastar(draw, grid, start, end):
    idx = 0
    open_set = [[], []]
    heapq.heappush(open_set[idx], (0, start))
    heapq.heappush(open_set[idx ^ 1], (0, end))
    came_from = [{}, {}]
    g_score = [{spot: float("inf") for row in grid for spot in row},
               {spot: float("inf") for row in grid for spot in row}]
    g_score[idx][start] = g_score[idx ^ 1][end] = 0
    f_score = [{spot: float("inf") for row in grid for spot in row},
               {spot: float("inf") for row in grid for spot in row}]
    f_score[idx][start] = f_score[idx ^ 1][end] = h(start.get_pos(), end.get_pos())

    open_set_hash = [{start}, {end}]

    pause = 0
    while len(open_set[0]) and len(open_set[1]):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bye()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause ^= 1
                elif event.key == pygame.K_q:
                    bye()
        if pause: continue
        if len(open_set[idx]) > len(open_set[idx ^ 1]): idx ^= 1
        current = heapq.heappop(open_set[idx])[1]
        open_set_hash[idx].remove(current)

        if current in open_set_hash[idx ^ 1]:
            print(current.row, current.col)
            reconstruct_path(came_from[0], current, draw)
            reconstruct_path(came_from[1], current, draw)
            # end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[idx][current] + (
                1 if neighbor.row == current.row or neighbor.col == current.col else math.sqrt(2))
            if neighbor.cost_idx: temp_g_score += EXTRA_COST[neighbor.cost_idx]
            if temp_g_score < g_score[idx][neighbor]:
                came_from[idx][neighbor] = current
                g_score[idx][neighbor] = temp_g_score
                f_score[idx][neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash[idx]:
                    heapq.heappush(open_set[idx], (f_score[idx][neighbor], neighbor))
                    open_set_hash[idx].add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start and current != end:
            current.make_closed()

    return False


def main(win, ROWS, COLS, GAP, grid, start=None, end=None):
    # 黄色格子代表沙漠，经过它的代价为 4 -- idx 2
    # 蓝色格子代表溪流，经过它的代价为 2 -- idx 1
    # 白色格子为普通地形，经过它的代价为 0 -- idx 0
    cost_idx = 0

    while True:
        draw(win, grid, ROWS, COLS, GAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bye()

            if pygame.mouse.get_pressed()[0]:  # LEFT
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

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
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
                    biastar(lambda: draw(win, grid, ROWS, COLS, GAP), grid, start, end)
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


if __name__ == "__main__":
    # 一个ROW*ROW的网格，ROW*gap = WIDTH像素
    # gap是每个方格的宽度
    ROWS = 20
    COLS = 40
    GAP = 34

    if len(sys.argv) > 1:
        grid, start, end, ROWS, COLS, GAP = load_map(sys.argv[1])
    else:
        start = None
        end = None
        grid = make_grid(ROWS, COLS, GAP)

    # 设置窗口宽和高
    pygame.init()
    WIDTH = COLS * GAP
    HEIGHT = ROWS * GAP
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bidirectional A* Path Finding Algorithm")

    main(WIN, ROWS, COLS, GAP, grid, start, end)