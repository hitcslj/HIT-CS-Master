import argparse
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


if __name__ == '__main__':
    args = get_parser()
    algo = searchAlgo(args.algo)
    WIN, ROWS, COLS, GAP, grid, start, end = init_map(args.data_path, args.algo)
    excute(algo, WIN, ROWS, COLS, GAP, grid, start, end)

# python main.py --algo astar --data_path map2.txt

# python main.py --algo biastar --data_path map2.txt
