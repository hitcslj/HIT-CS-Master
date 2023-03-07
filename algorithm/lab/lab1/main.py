from convexHull import convexHull
from utils import createData,plot_performance_curve
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='convex hull algorithm')
    parser.add_argument('--algo',
                        type=str,
                        default='grahamScan',
                        help='algorithm name:bruteForce, grahamScan,div')
    args = parser.parse_args()
    algorithm = convexHull(args.algo) #'bruteForce', 'grahamScan', 'div'
    datasets = createData(sizes=[1000, 2000, 3000])
    plot_performance_curve(algorithm, datasets)


# python main.py --name 'grahamScan'
