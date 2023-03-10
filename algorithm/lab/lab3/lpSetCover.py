from pulp import *

def lpSetCover(data):
    """
       使用线性规划松弛算法来解决集合覆盖问题
       :param data: 全集,子集列表
       :return: 最小的子集列表，使得它们的并集等于全集
       """
    universe,subsets = data
    subsets = [tuple(s) for s in subsets]
    # 创建线性规划问题
    problem = LpProblem('Set_Cover', LpMinimize)

    # 创建决策变量，0代表集合不选，1代表集合选
    subset_vars = LpVariable.dicts('Subset', subsets, lowBound=0, cat='Binary')

    # 添加目标函数，使得选择集合的个数最少
    problem += lpSum([subset_vars[s] for s in subsets])

    # 添加约束条件，每个元素都要被所选子集至少包含一次
    for e in universe:
        problem += lpSum([subset_vars[s] for s in subsets if e in s]) >= 1

    # 解决线性规划问题
    problem.solve()

    # 获取解决方案
    selected_subsets = [s for s in subsets if subset_vars[s].value() == 1]

    return selected_subsets

if __name__=='__main__':
    universe = {1, 2, 3, 4, 5}
    subsets = [{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]
    data = universe, subsets
    print(lpSetCover(data))