import time
import matplotlib.pyplot as plt
import random

# 计算向量AB和向量AP的叉积.负(P在AB下方)，正（P在AB上方）
def cross_product(A, B, P):
    return (B[0] - A[0])*(P[1] - A[1]) - (P[0] - A[0]) * (B[1] - A[1])


# 输入的点都是凸包上点顶点，输出按照逆时针顺序返回点凸包
def convex_hull(points):
    pivot = min(points, key=lambda p: (p.y, p.x))
    sorted_points = sorted(points, key=lambda p: cmp_points(p, pivot))
    stack = [pivot, sorted_points[1]]
    for p in sorted_points[2:]:
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