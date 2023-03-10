import time
import matplotlib.pyplot as plt
import random

def createData(sizes=[]):
    """
    生成指定数量的数据
    :param sizes: 数据规模大小数组
    :return: 指定数量的数据
    """
    datasets = []
    for size in sizes:
        data = generate_instance(size, size)
        datasets.append(data)
    return datasets

def generate_instance(num_points, num_sets):
    # 随机生成X集合
    universe = set(range(num_points))
    # 生成可行解集合
    feasible_sets = []
    current_set = set(random.sample(universe, 20))
    feasible_sets.append(current_set)
    curNum = 1
    while len(universe - set().union(*feasible_sets)) >= 20 and curNum+1<num_sets:
        n = random.randint(1, min(20, num_points - len(current_set), len(current_set)))
        x = random.randint(1, n)
        next_set = set(random.sample(universe - current_set, x))
        next_set |= set(random.sample(current_set, n - x))
        current_set = next_set
        feasible_sets.append(current_set)
    feasible_sets.append(universe-set().union(*feasible_sets))
    # 随机生成其余集合
    remaining_sets = []
    while len(remaining_sets) < num_sets - len(feasible_sets):
        s = set(random.sample(universe, random.randint(1, num_points // 2)))
        if s not in feasible_sets and s not in remaining_sets:
            remaining_sets.append(s)

    # 合并可行解集合和其余集合
    subsets = feasible_sets + remaining_sets

    return universe, subsets

def run_algorithm(algorithm, data): #测试算法运行时间
    start_time = time.time()
    algorithm(data)
    end_time = time.time()
    return (end_time - start_time) * 1000

def plot_performance_curve(algorithm, data_sets):
    sizes = [len(data[0]) for data in data_sets]
    times = [run_algorithm(algorithm, data) for data in data_sets]
    plt.plot(sizes, times, '-o')
    plt.xlabel("Data Size")
    plt.ylabel("Running Time (ms)")
    plt.title("Performance Curve for {}".format(algorithm.__name__))
    plt.savefig("Performance_Curve_for_{}".format(algorithm.__name__))
    plt.show()

if __name__=='__main__':
    data = generate_instance(1000,1000)
    print(data)