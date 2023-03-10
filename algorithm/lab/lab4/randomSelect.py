import random

def randomSelect(nums):
    return select_kth_smallest(nums,2)


def select_kth_smallest(arr, k):
    pivot = random.choice(arr)
    lows = [el for el in arr if el < pivot]
    highs = [el for el in arr if el > pivot]
    pivots = [el for el in arr if el == pivot]

    if k <= len(lows):
        return select_kth_smallest(lows, k)
    elif k > len(lows) + len(pivots):
        return select_kth_smallest(highs, k - len(lows) - len(pivots))
    else:
        return pivot

if __name__=='__main__':
    nums = [3,2,1,5,6,4]
    pivot = randomSelect(nums)
    print(pivot)