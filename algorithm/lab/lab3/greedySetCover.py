def greedySetCover(data):
    """
    使用贪心算法来解决集合覆盖问题
    :param data: 全集,子集列表
    :return: 最小的子集列表，使得它们的并集等于全集
    """
    universe, subsets = data

    # 存储所有被覆盖的元素
    covered = set()

    # 存储选中的子集
    selected_subsets = []

    # 如果还有元素没有被覆盖
    while covered != universe:
        # 选择未被覆盖元素最多的子集
        subset = max(subsets, key=lambda s: len(s - covered))

        # 将这个子集加入到被选中的子集列表中
        selected_subsets.append(subset)

        # 将这个子集覆盖的元素加入到已被覆盖的元素列表中
        covered |= subset

    return selected_subsets

if __name__=='__main__':
    universe = {1, 2, 3, 4, 5}
    subsets = [{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]
    data = universe, subsets
    print(greedySetCover(data))