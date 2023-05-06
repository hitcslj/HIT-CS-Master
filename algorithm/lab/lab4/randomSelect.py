import random

def randomSelect(nums):
    return lazy_select(nums,2)


def rank(arr, x):
    return sum(1 for el in arr if el <= x)


def lazy_select(S, k):
    n = len(S)
    while True:
        m = int(n**(3/4))
        R = random.sample(S, k=m)
        R.sort()
        x = int(k/n*m)
        gap = int(n**(1/2))

        l = max(x - gap, 0)
        h = min(x + gap, m-1)

        L = R[l]
        H = R[h]

        Lp = rank(S, L)
        Hp = rank(S, H)

        P = [y for y in S if L <= y <= H]

        if Lp <= k <= Hp and len(P) <= 4 * n**(3/4) + 1:
            P.sort()
            return P[k - Lp]

if __name__=='__main__':
    nums = [3,2,1,5,6,4]
    pivot = randomSelect(nums)
    print(pivot)