from convexHull import convexHull
from utils import createData, plot_performance_curve
import argparse

parser = argparse.ArgumentParser(description='convex hull algorithm')
parser.add_argument('--algo',
                    type=str,
                    default='grahamScan',
                    help='algorithm name: bruteForce, grahamScan,div')
parser.add_argument('--sizes',
                    type=str,
                    default='1000,2000,3000',
                    help='sizes for data')
args = parser.parse_args()

if __name__ == '__main__':
    algo_name = args.algo
    sizes = list(map(int, args.sizes.split(',')))
    algorithm = convexHull(algo_name)
    datasets = createData(sizes)
    plot_performance_curve(algorithm, datasets)

# python main.py --algo bruteForce --sizes 10,20,30

# python main.py --algo grahamScan --sizes 1000,2000,3000

# python main.py --algo div --sizes 1000,2000,3000

