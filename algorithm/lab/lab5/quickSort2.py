import random
from typing import List


def quickSort2(nums) -> List[int]:
    if len(nums) <= 1:
        return nums
    mid = random.randint(0, len(nums) - 1)
    pivot = nums[mid]  # 随机选择一个枢轴元素
    left = [x for x in nums if x < pivot]
    middle = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quickSort2(left) + middle + quickSort2(right)


if __name__ == '__main__':
    nums = [1, 7, 3, 5, 4, 2, 2]
    # nums = [10] * (10 ** 4)
    nums = quickSort2(nums)
    print(nums)
