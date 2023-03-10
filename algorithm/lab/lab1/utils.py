import time
import matplotlib.pyplot as plt
import random


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
    plt.savefig("Performance_Curve_for_{}".format(algorithm.__name__))
    plt.show()