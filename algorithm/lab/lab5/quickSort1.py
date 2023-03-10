import random
import sys

sys.setrecursionlimit(100000)


def quickSort1(nums):
    n = len(nums)
    quickSort(nums, 0, n - 1)


def quickSort(nums, l, r):
    if l < r:
        mid = randomPartition(nums, l, r)
        quickSort(nums, l, mid - 1)
        quickSort(nums, mid + 1, r)


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


if __name__ == '__main__':
    nums = [1, 7, 3, 5, 4, 2, 2]
    # nums = [10]*(10000)
    quickSort1(nums)
    print(nums[:100])
