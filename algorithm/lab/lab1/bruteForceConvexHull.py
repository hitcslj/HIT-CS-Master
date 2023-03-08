from utils import cross_product

# 判断点P是否在三角形ABC内
def in_triangle(A, B, C, P):
    return (cross_product(A, B, P) * cross_product(A, B, C) > 0 and
            cross_product(A, C, P) * cross_product(A, C, B) > 0 and
            cross_product(B, C, P) * cross_product(B, C, A) > 0)


def in_any_triangle(P, points):
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                A, B, C = points[i], points[j], points[k]
                if P not in [A, B, C] and in_triangle(A, B, C, P):
                    # print(P,A,B,C)
                    return True
    return False


def bruteForceConvexHull(points):
    n = len(points)
    if n < 3:
        return points
    flag = [True] * n
    for i, p in enumerate(points):
        if in_any_triangle(p, points):
            flag[i] = False
    hull = [p for i, p in enumerate(points) if flag[i]]
    # 对凸包的顶点按照极角排序
    hull.sort(key=lambda p: (p[1], p[0]))
    hull = hull[:3] + sorted(hull[3:], key=lambda p: -cross_product(hull[0], hull[1], p))
    return hull

if __name__ == '__main__':
    points = [[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]
    outputs = bruteForceConvexHull(points)
    # print(outputs)
    target = [[1, 1], [2, 0], [3, 3], [2, 4], [4, 2]]
    print(sorted(target) == sorted(outputs))
