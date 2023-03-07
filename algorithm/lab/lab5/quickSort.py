import random
from typing import *

def quickSort(nums):
    n = len(nums)
    quickSort1(nums, 0, n - 1)
    # quickSort2(nums,0, n-1)

def quickSort1(nums, l, r):
    if l < r:
        mid = randomPartition(nums, l, r)
        quickSort1(nums, l, mid - 1)
        quickSort1(nums, mid + 1, r)


def randomPartition(nums, l, r):
    i = random.randint(l, r)  # 随机一个分割点
    nums[i], nums[r] = nums[r], nums[i]  # 交换到末尾
    pivot = nums[r]  # 作为中枢值,进行划分。
    i = l - 1
    for j in range(l, r):
        if nums[j] <= pivot:  # 通过此步骤将<=pivot的数字都搬到前面来
            i += 1
            nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1], nums[r] = nums[r], nums[i + 1]  # 将pivot放到它应该的位置
    return i + 1  # 返回中枢值的索引


def quickSort2(nums) -> List[int]:
    if len(nums) <= 1:
        return nums
    pivot = nums[len(nums) // 2]  # 随机选择一个枢轴元素
    left = [x for x in nums if x < pivot]
    middle = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quickSort2(left) + middle + quickSort2(right)


if __name__ == '__main__':
    nums = list(range(10000))
    random.shuffle(nums)
    quickSort(nums)
    # print(nums[:100])

