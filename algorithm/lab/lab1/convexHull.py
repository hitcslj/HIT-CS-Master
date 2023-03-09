from bruteForceConvexHull import bruteForceConvexHull
from divConvexHull import divConvexHull
from grahamScanConvexHull import grahamScanConvexHull


def convexHull(method='bruteForce'):
    if method == 'bruteForce':
        return bruteForceConvexHull # T(n) = O(n^4)
    elif method == 'grahamScan':
        return grahamScanConvexHull # T(n) = O(nlogn)
    else:
        return divConvexHull # T(n) = O(nlogn)
