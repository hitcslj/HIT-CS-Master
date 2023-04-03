import math


def f_a(x):
    return 2 * x ** 2 - x - 1


def f_b(x):
    return 3 * x ** 2 - 21.6 * x - 1


def golden_section_search(f, a, b, delta):
    golden_ratio = (math.sqrt(5) - 1) / 2
    k = 0
    while b - a > delta:
        c = a + (1 - golden_ratio) * (b - a)
        d = a + golden_ratio * (b - a)
        if f(c) < f(d):
            b = d
        else:
            a = c
        k += 1
    return (a + b) / 2, k


def fibonacci_search(f, a, b, delta):
    n = 0
    fib = [1, 1]
    k = 0
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
        k += 1
    return (a + b) / 2, k


def bisection_search(f, a, b, delta):
    k = 0
    while b - a > delta:
        c = (a + b) / 2
        fc = f(c)
        fd = f(c + delta * (1e-5))
        if fc < fd:  # 用差分代替导数,导数大于零时函数单调递增
            b = c
        else:
            a = c
        k += 1
    return (a + b) / 2, k


def dichotomous_search(f, a, b, delta):
    k = 0
    while b - a > delta:
        k += 1
        c = (a + b) / 2 - delta / 4
        d = (a + b) / 2 + delta / 4
        if f(c) < f(d):
            b = d
        else:
            a = c
    return (a + b) / 2, k


import numpy as np


class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def _get_sp_intersection(A: Pt, B: Pt, l: float) -> Pt:
    x = ((A.y - B.y) + l * (A.x + B.x)) / (2 * l)
    return Pt(x, A.y - l * (x - A.x))


def shubert_piyavskii(f, a, b, l, delta=0.01, eps=1e-5, ):
    m = (a + b) / 2
    A, M, B = Pt(a, f(a)), Pt(m, f(m)), Pt(b, f(b))
    pts = [A, _get_sp_intersection(A, M, l), M, _get_sp_intersection(M, B, l), B]
    diff = np.inf
    k = 0
    while diff > eps:
        i = np.argmin([P.y for P in pts if P.x not in [a, m, b]])
        P = Pt(pts[i].x, f(pts[i].x))
        diff = P.y - pts[i].y  # 下界的最小值和f(x)的差值
        P_prev = _get_sp_intersection(pts[i - 1], P, l)
        P_next = _get_sp_intersection(P, pts[i + 1], l)
        k += 1
        if (P_next.x - P_prev.x) < delta:
            return P.x, k
        del pts[i]
        pts.insert(i, P_next)
        pts.insert(i, P)
        pts.insert(i, P_prev)
    return None


# Problem a
a0, b0, delta_a = -1, 1, 0.06
# Problem b
a1, b1, delta_b = 0, 25, 0.08

problems = {
    "a": (f_a, a0, b0, delta_a),
    "b": (f_b, a1, b1, delta_b)
}

methods = {
    "Golden Section Search": golden_section_search,
    "Fibonacci Search": fibonacci_search,
    "Bisection Search": bisection_search,
    "Dichotomous Search": dichotomous_search,
    "Shubert-Piyavskii": lambda f, a, b, delta: shubert_piyavskii(f, a, b, l=5, delta=delta)
}

with open("result_2.txt", "w") as file:
    for problem_name, (f, a, b, delta) in problems.items():
        print(f"Problem {problem_name}:\n", file=file)
        for method_name, method in methods.items():
            x_min, iterations = method(f, a, b, delta=delta)
            x_min = np.round(x_min, 2)
            y_min = np.round(f(x_min), 2)
            output = f"{method_name} - Minimum value: {y_min} at {x_min} - iterations : {iterations}\n"
            print(output)
            print(output, file=file)