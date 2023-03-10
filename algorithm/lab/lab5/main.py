from utils import createData,plot_performance_curve
from quickSort import quickSort
import argparse

parser = argparse.ArgumentParser(description='convex hull algorithm')
parser.add_argument('--algo',
                    type=str,
                    default='quickSort1',
                    help='algorithm name: quickSort1, quickSort2')
parser.add_argument('--size',
                    type=int,
                    default=10000,
                    help='size for data')
args = parser.parse_args()

if __name__ == '__main__':
    algo_name = args.algo
    size = args.size
    algorithm = quickSort(algo_name)
    datasets = createData(N=size)
    plot_performance_curve(algorithm, datasets)


