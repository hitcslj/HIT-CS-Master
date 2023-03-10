from astar import astar
from biastar import biastar

def searchAlgo(method='astar'):
    if method == 'astar':
        return astar
    elif method == 'biastar':
        return biastar
    else:
        raise ValueError("method must in [astar,biastar]")