import random

def divSelect(nums):
    k = 2  #这里的k在[1,len(nums)]之间即可，简单设置为2
    return quickselect(nums, k)

def quickselect(arr, k):
    randomIdx = random.randint(0, len(arr) - 1)
    pivot = arr[randomIdx]
    left, right, mid = [], [], []
    for num in arr:
        if num < pivot:
            left.append(num)
        elif num > pivot:
            right.append(num)
        else:
            mid.append(num)
    if len(left) >= k:
        pivot = quickselect(left, k)
    elif len(left) + len(mid) < k:
        pivot = quickselect(right, k - len(left) - len(mid))
    return pivot

if __name__=='__main__':
    nums = [3,2,1,5,6,4]
    pivot = divSelect(nums)
    print(pivot)
