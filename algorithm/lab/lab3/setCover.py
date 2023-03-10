from greedySetCover import greedySetCover
from lpSetCover import lpSetCover


def setCover(method='greedySetCover'):
    if method == 'greedySetCover':
        return greedySetCover
    elif method == 'lpSetCover':
        return lpSetCover
    else:
        raise ValueError("method must in [greedySetCover,lpSetCover]")
