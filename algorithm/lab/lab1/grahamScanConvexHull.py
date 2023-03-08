from functools import cmp_to_key
from typing import *


def grahamScanConvexHull(points):
    def cross(p: List[int], q: List[int], r: List[int]) -> int:
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    def distance(p: List[int], q: List[int]) -> int:
        return (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1])

    n = len(points)
    if n < 4:
        return points

    # 找到 y 最小的点 bottom
    bottom = 0
    for i, point in enumerate(points):
        if point[1] < points[bottom][1]:
            bottom = i
    points[bottom], points[0] = points[0], points[bottom]

    # 以 bottom 原点，按照极坐标的角度大小进行排序
    def cmp(a: List[int], b: List[int]) -> int:
        diff = - cross(points[0], a, b)
        return diff if diff else distance(points[0], a) - distance(points[0], b)

    points[1:] = sorted(points[1:], key=cmp_to_key(cmp))

    # 对于凸包最后且在同一条直线的元素按照距离从大到小进行排序
    r = n - 1
    while r >= 0 and cross(points[0], points[n - 1], points[r]) == 0:
        r -= 1
    l, h = r + 1, n - 1
    while l < h:
        points[l], points[h] = points[h], points[l]
        l += 1
        h -= 1

    stack = [0, 1]
    for i in range(2, n):
        # 如果当前元素与栈顶的两个元素构成的向量顺时针旋转，则弹出栈顶元素
        while len(stack) > 1 and cross(points[stack[-2]], points[stack[-1]], points[i]) < 0:
            stack.pop()
        stack.append(i)
    return [points[i] for i in stack]


if __name__ == '__main__':
    points = [[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]
    outputs = grahamScanConvexHull(points)
    target = [[1, 1], [2, 0], [3, 3], [2, 4], [4, 2]]
    print(sorted(target) == sorted(outputs))
