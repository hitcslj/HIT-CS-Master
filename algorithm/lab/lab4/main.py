from utils import createData,plot_performance_curve
from findKthSmall import findKthSmall
import argparse

parser = argparse.ArgumentParser(description='quick select algorithm')
parser.add_argument('--algo',
                    type=str,
                    default='divSelect',
                    help='algorithm name: divSelect, randomSelect')

parser.add_argument('--sizes',
                    type=str,
                    default='1000,2000,5000,10000,20000,50000,100000',
                    help='sizes for data')

args = parser.parse_args()

if __name__ == '__main__':
    algo_name = args.algo
    sizes = list(map(int, args.sizes.split(',')))
    algorithm = findKthSmall(algo_name)
    datasets = createData(sizes)
    plot_performance_curve(algorithm, datasets)


