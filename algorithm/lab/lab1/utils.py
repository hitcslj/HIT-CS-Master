import time
from functools import cmp_to_key
import matplotlib.pyplot as plt
import random
from typing import *




# 输入的点都是凸包上点顶点，输出按照逆时针顺序返回点凸包
def convex_hull(points):
    pivot = min(points, key=lambda p: (p.y, p.x))
    def distance(p: List[int], q: List[int]) -> int:
        return (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1])
    def cmp(a: List[int], b: List[int]) -> int:
        diff = - cross_product(points[0], a, b)
        return diff if diff else distance(points[0], a) - distance(points[0], b)

    points[1:] = sorted(points[1:], key=cmp_to_key(cmp))

    stack = [pivot, points[1]]
    for p in points[2:]:
        while len(stack) >= 2 and cross_product(stack[-2],stack[-1],p) < 0:
            stack.pop()
        stack.append(p)
    return stack

def createData(sizes=[]):
    """
    生成指定数量的随机点
    :param sizes: 需要生成的点数的数组
    :return: 生成的点列表
    """
    datasets = []
    for size in sizes:
        points = []
        for i in range(size):
            x = random.uniform(0, 100)  # 生成x坐标
            y = random.uniform(0, 100)  # 生成y坐标
            points.append((x, y))
        datasets.append(points)
    return datasets

def run_algorithm(algorithm, data): #测试算法运行时间
    start_time = time.time()
    algorithm(data)
    end_time = time.time()
    return (end_time - start_time) * 1000

def plot_performance_curve(algorithm, data_sets):
    sizes = [len(data) for data in data_sets]
    times = [run_algorithm(algorithm, data) for data in data_sets]
    plt.plot(sizes, times, '-o')
    plt.xlabel("Data Size")
    plt.ylabel("Running Time (ms)")
    plt.title("Performance Curve for {}".format(algorithm.__name__))
    plt.savefig("Performance Curve for {}".format(algorithm.__name__))
    plt.show()