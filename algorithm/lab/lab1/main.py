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
    sizes = [1000, 2000, 3000]
    if args.algo=='bruteForce': #暴力太慢了，所以将size减小，好出图
        sizes = [10,20,30]
    datasets = createData(sizes)
    plot_performance_curve(algorithm, datasets)


# python main.py --algo 'grahamScan'
