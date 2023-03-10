import argparse
import time
from utils import *
from searchAlgo import searchAlgo

def get_parser():
    parser = argparse.ArgumentParser(description='A star search algorithm')
    parser.add_argument('--algo',
                        type=str,
                        default='astar',
                        help='algorithm name: astar, biastar')
    parser.add_argument('--data_path',
                        type=str,
                        default='map1.txt',
                        help='data path')
    args = parser.parse_args()
    return args

def main(algorithm, win, ROWS, COLS, GAP, grid, start=None, end=None):
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
                    algorithm(lambda: draw(win, grid, ROWS, COLS, GAP), grid, start, end)
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


if __name__ == '__main__':
    args = get_parser()
    algo = searchAlgo(args.algo)
    WIN, ROWS, COLS, GAP,grid,start,end = init_map(args.data_path,args.algo)
    main(algo,WIN, ROWS, COLS, GAP, grid, start, end)

# python main.py --algo astar --data_path map2.txt

# python main.py --algo biastar --data_path map2.txt



