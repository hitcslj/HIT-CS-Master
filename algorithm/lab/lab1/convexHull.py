from bruteForceConvexHull import bruteForceConvexHull
from divConvexHull import divConvexHull
from grahamScanConvexHull import grahamScanConvexHull

def convexHull(method='bruteForce'):
    if method == 'bruteForce':
        return bruteForceConvexHull
    elif method == 'grahamScan':
        return grahamScanConvexHull
    else:
        return divConvexHull

