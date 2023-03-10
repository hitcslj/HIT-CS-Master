from quickSort1 import quickSort1
from quickSort2 import quickSort2


def quickSort(method='quickSort1'):
    if method == 'quickSort1':
        return quickSort1
    elif method == 'quickSort2':
        return quickSort2
    else:
        raise ValueError("method must in [quickSort1,quickSort2]")
