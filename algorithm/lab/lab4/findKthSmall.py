from divSelect import divSelect
from randomSelect import randomSelect

def findKthSmall(method='divSelect'):
    if method == 'divSelect':
        return divSelect
    elif method == 'randomSelect':
        return randomSelect
    else:
        raise ValueError("method must in [divSelect,randomSelect]")