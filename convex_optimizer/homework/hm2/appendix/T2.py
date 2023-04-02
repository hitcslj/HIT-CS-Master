import math

def f_a(x):
    return 2 * x**2 - x - 1

def f_b(x):
    return 3 * x**2 - 21.6 * x - 1

def golden_section_search(f, a, b, delta):
    golden_ratio = (math.sqrt(5) - 1) / 2
    while b - a > delta:
        c = a + (1-golden_ratio) * (b - a)
        d = a + golden_ratio * (b - a)
        if f(c) < f(d):
            b = d
        else:
            a = c
    return (a + b) / 2

def fibonacci_search(f, a, b, delta):
    n = 0
    fib = [1, 1]
    while fib[-1] < (b - a) / delta:
        fib.append(fib[-1] + fib[-2])
        n += 1
    while n > 0:
        c = a + fib[n - 1] / fib[n + 1] * (b - a)
        d = a + fib[n] / fib[n + 1] * (b - a)
        if f(c) < f(d):
            b = d
        else:
            a = c
        n -= 1
    return (a + b) / 2

def bisection_search(f, a, b, delta):
    while b - a > delta:
        c = (a + b) / 2
        fc = f(c)
        fd = f(c + delta*(1e-5))
        if fc < fd: #用差分代替导数,导数大于零时函数单调递增
            b = c
        else:
            a = c
    return (a + b) / 2

def dichotomous_search(f, a, b, delta):
    while b - a > delta:
        c = (a + b) / 2 - delta / 4
        d = (a + b) / 2 + delta / 4
        if f(c) < f(d):
            b = d
        else:
            a = c
    return (a + b) / 2

import numpy as np

class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def _get_sp_intersection(A: Pt, B: Pt, l: float) -> Pt:
    x = ((A.y - B.y) + l * (A.x + B.x)) / (2 * l)
    return Pt(x, A.y - l*(x - A.x))

def shubert_piyavskii(f, a, b, l, delta=0.01,eps=1e-5, ):
    m = (a + b) / 2
    A, M, B = Pt(a, f(a)), Pt(m, f(m)), Pt(b, f(b))
    pts = [A, _get_sp_intersection(A, M, l), M, _get_sp_intersection(M, B, l), B]
    diff = np.inf
    while diff > eps:
        i = np.argmin([P.y for P in pts if P.x not in [a,m,b]])
        P = Pt(pts[i].x, f(pts[i].x))
        diff = P.y - pts[i].y #下界的最小值和f(x)的差值
        P_prev = _get_sp_intersection(pts[i - 1], P, l)
        P_next = _get_sp_intersection(P, pts[i + 1], l)
        if (P_next.x - P_prev.x) < delta:
            return P.x
        del pts[i]
        pts.insert(i, P_next)
        pts.insert(i, P)
        pts.insert(i, P_prev)
    return None


# Problem a
a0, b0, delta_a = -1, 1, 0.06
# Problem b
a1, b1, delta_b = 0, 25, 0.08

# Solve problem a
print("Problem a:")
print("Golden Section Search:", golden_section_search(f_a, a0, b0, delta_a))
print("Fibonacci Search:", fibonacci_search(f_a, a0, b0, delta_a))
print("Bisection Search:", bisection_search(f_a, a0, b0, delta_a))
print("Dichotomous Search:", dichotomous_search(f_a, a0, b0, delta_a))
print("Shubert-Piyavskii (L = 5):", shubert_piyavskii(f_a, a0, b0, l=5,delta=delta_a ))

# Solve problem b
print("\nProblem b:")
print("Golden Section Search:", golden_section_search(f_b, a1, b1, delta_b))
print("Fibonacci Search:", fibonacci_search(f_b, a1, b1, delta_b))
print("Bisection Search:", bisection_search(f_b, a1, b1, delta_b))
print("Dichotomous Search:", dichotomous_search(f_b, a1, b1, delta_b))
print("Shubert-Piyavskii (L = 150):", shubert_piyavskii(f_b, a1, b1, l=150,delta=delta_b))

# 将上面打印结果保存到result_2.txt
with open('result_2.txt', 'w') as f:
    # Solve problem a
    print("Problem a:", file=f)
    print("Golden Section Search:", golden_section_search(f_a, a0, b0, delta_a), file=f)
    print("Fibonacci Search:", fibonacci_search(f_a, a0, b0, delta_a), file=f)
    print("Bisection Search:", bisection_search(f_a, a0, b0, delta_a), file=f)
    print("Dichotomous Search:", dichotomous_search(f_a, a0, b0, delta_a), file=f)
    print("Shubert-Piyavskii (L = 5):", shubert_piyavskii(f_a, a0, b0, l=5, delta=delta_a), file=f)

    # Solve problem b
    print("\nProblem b:", file=f)
    print("Golden Section Search:", golden_section_search(f_b, a1, b1, delta_b), file=f)
    print("Fibonacci Search:", fibonacci_search(f_b, a1, b1, delta_b), file=f)
    print("Bisection Search:", bisection_search(f_b, a1, b1, delta_b), file=f)
    print("Dichotomous Search:", dichotomous_search(f_b, a1, b1, delta_b), file=f)
    print("Shubert-Piyavskii (L = 150):", shubert_piyavskii(f_b, a1, b1, l=150, delta=delta_b), file=f)
