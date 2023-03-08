from utils import cross_product

def merge(left_hull, right_hull):
    """
    将左右两个凸包合并成一个凸包
    """
    # 找到左凸包中y坐标最小的点
    left_min_y = min(p[1] for p in left_hull)
    p1 = [p for p in left_hull if p[1] == left_min_y][0]
    p_x = [p1[0]+1,p1[0]] #和p1在同一水平线的点
    # 将凸包的点按照极角排序
    sorted_points = []
    for hull in (left_hull, right_hull):
        upper_hull = []
        lower_hull = []
        for p in hull:
            # 如果点在 p1 和 p2 形成的三角形内部，则将点分别加入到上凸包和下凸包
            if cross_product(p1, p_x, p) < 0:
                upper_hull.append(p)
            elif cross_product(p1, p_x, p) > 0:
                lower_hull.append(p)

        # 将上凸包和下凸包分别按照 x 坐标递增排序
        upper_hull.sort(key=lambda p: p[0])
        lower_hull.sort(key=lambda p: p[0], reverse=True)

        # 将上凸包和下凸包中的点按照顺序加入到排序点列表中
        sorted_points += upper_hull + lower_hull

    # 从排序点列表中构造合并后的凸包
    merged_hull = []
    for p in sorted_points:
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