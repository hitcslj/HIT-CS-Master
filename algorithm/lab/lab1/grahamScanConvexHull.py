from typing import *
from math import *
def grahamScanConvexHull(points):
    def cross_product(A, B, P):
        # 计算向量AB和向量BP的叉积
        return (B[0] - A[0]) * (P[1] - B[1]) - (P[0] - B[0]) * (B[1] - A[1])

    def distance(p: List[int], q: List[int]) -> int:
        return (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1])

    n = len(points)
    if n < 3:
        return points
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
    # 使用栈进行扫描
    stack = [points[0], points[1]]
    for i in range(2, n):
        while len(stack) >= 2 and cross_product(stack[-2], stack[-1], points[i]) < 0:
            stack.pop()
        stack.append(points[i])
    return stack


if __name__ == '__main__':
    points = [[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]
    outputs = grahamScanConvexHull(points)
    target = [[1, 1], [2, 0], [3, 3], [2, 4], [4, 2]]
    print(sorted(target) == sorted(outputs))









