from setCover import setCover
from utils import createData, plot_performance_curve
import argparse

parser = argparse.ArgumentParser(description='mini set Cover algorithm')
parser.add_argument('--algo',
                    type=str,
                    default='greedySetCover',
                    help='algorithm name: greedySetCover, lpSetCover')
parser.add_argument('--sizes',
                    type=str,
                    default='100,200,300,400,500,1000,2000',
                    help='sizes for data')

args = parser.parse_args()

if __name__ == '__main__':
    algo_name = args.algo
    sizes = list(map(int, args.sizes.split(',')))
    algorithm = setCover(algo_name)
    datasets = createData(sizes)
    plot_performance_curve(algorithm, datasets)

# python main.py --algo greedySetCover --sizes 100,200,300,400,500,1000,2000

# python main.py --algo lpSetCover --sizes 100,200,300,400,500,1000,2000



