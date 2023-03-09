from math import *
from typing import *


def cross_product(A, B, P):
    # 计算向量AB和向量BP的叉积
    return (B[0] - A[0]) * (P[1] - B[1]) - (P[0] - B[0]) * (B[1] - A[1])


def distance(p: List[int], q: List[int]) -> int:
    return (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1])


def merge(left_hull, right_hull):
    """
    将左右两个凸包合并成一个凸包,准确来说应该是用三指针归并，我这里偷懒了，导致负责度变为了O(n(logn)^2)
    """
    points = left_hull + right_hull
    n = len(points)
    # 找到最下面中最左边的点
    points.sort(key=lambda p: (p[1], p[0]))
    # 将所有点按照与最下面的点的极角排序
    points[1:] = sorted(points[1:],
                        key=lambda p: (atan2(p[1] - points[0][1], p[0] - points[0][0]), distance(p, points[0])))

    # 对于凸包最后且在同一条直线的元素按照距离从大到小进行排序
    r = n - 1
    while r >= 0 and cross_product(points[0], points[n - 1], points[r]) == 0:
        r -= 1
    l, h = r + 1, n - 1
    while l < h:
        points[l], points[h] = points[h], points[l]
        l += 1
        h -= 1
    # 从排序点列表中构造合并后的凸包
    merged_hull = [points[0], points[1]]
    for p in points[2:]:
        while len(merged_hull) >= 2 and cross_product(merged_hull[-2], merged_hull[-1], p) < 0:
            merged_hull.pop()
        merged_hull.append(p)
    return merged_hull

def divConvexHull(points):
    """
    使用分治算法求解凸包
    """
    n = len(points)
    if n < 4:
        # 找到最下面中最左边的点
        points.sort(key=lambda p: (p[1], p[0]))
        # 将所有点按照与最下面的点的极角排序
        points[1:] = sorted(points[1:],
                            key=lambda p: (atan2(p[1] - points[0][1], p[0] - points[0][0])))
        return points

    # 将点集按照 x 坐标排序，并将其分为左右两部分
    sorted_points = sorted(points)
    left_points = sorted_points[:n // 2]
    right_points = sorted_points[n // 2:]

    # 递归求解左右两部分的凸包
    left_hull = divConvexHull(left_points)
    right_hull = divConvexHull(right_points)
    # 将左右两个凸包合并成一个凸包
    return merge(left_hull, right_hull)


if __name__ == '__main__':
    points = [[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]
    outputs = divConvexHull(points)
    print(outputs)
    target = [[1, 1], [2, 0], [3, 3], [2, 4], [4, 2]]
    print(sorted(target) == sorted(outputs))
