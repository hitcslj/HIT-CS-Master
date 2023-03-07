import random
import time
import matplotlib.pyplot as plt
import numpy as np

def createData(flag=False,n=11): #flag表示是否记录文件
    data_sets = []
    N = 10**4 # N用来调整一组数据的size
    for i in range(n):
        percentage = i * 10
        num_duplicates = (percentage * N) // 100
        data = [random.randint(1, N) for _ in range(N - num_duplicates+1)]#加一是防止为空
        data += [random.choice(data) for _ in range(num_duplicates)]
        random.shuffle(data)
        data_sets.append(data)
    if flag:
        # 将数据集写入文件
        with open("data.txt", "w") as f:
            for data in data_sets:
                np.savetxt(f, np.array(data).reshape(1, -1), fmt="%d")
    return data_sets

def run_algorithm(algorithm, data): #测试算法运行时间
    start_time = time.time()
    algorithm(data)
    end_time = time.time()
    return (end_time - start_time) * 1000

def plot_performance_curve(algorithm, data_sets):
    sizes = [len(data)-len(set(data))+1 for data in data_sets]
    times = [run_algorithm(algorithm, data) for data in data_sets]
    plt.plot(sizes, times, '-o')
    plt.xlabel("Data duplicate Size")
    plt.ylabel("Running Time (ms)")
    plt.title("Performance Curve for {}".format(algorithm.__name__))
    plt.savefig("quicksort_performance.png")
    plt.show()

