import numpy as np
from scipy.optimize import minimize_scalar

# 测试函数定义
def quadratic(x):
    a, b, c = 2, -3, 1
    return a * x**2 + b * x + c

def cubic(x):
    a, b, c, d = 1, -2, 1, 2
    return a * x**3 + b * x**2 + c * x + d

def quartic(x):
    a, b, c, d, e = 1, -2, 1, 2, 1
    return a * x**4 + b * x**3 + c * x**2 + d * x + e

def rosenbrock(x):
    a, b = 1, 100
    return (a - x)**2 + b * (x**2 - x)**2

def rastrigin(x):
    A = 10
    return A + x**2 - A * np.cos(2 * np.pi * x)

def ackley(x):
    a, b = 20, 0.2
    return -a * np.exp(-b * np.sqrt(x**2 / 2)) - np.exp(np.cos(2 * np.pi * x) / 2) + a + np.exp(1)

def griewank(x):
    return 1 + x**2 / 4000 - np.cos(x)

def schwefel(x):
    return 418.9829 - x * np.sin(np.sqrt(np.abs(x)))

test_functions = [quadratic, cubic, quartic, rosenbrock, rastrigin, ackley, griewank, schwefel]

methods = ['golden', 'fibonacci', 'brent', 'bounded']  # SciPy库提供的一维搜索方法

for i, func in enumerate(test_functions):
    print(f"测试函数{i + 1}:")
    for method in methods:
        result = minimize_scalar(func, method=method, bounds=(-5, 5)) if method == 'bounded' else minimize_scalar(func, method=method)
        print(f"{method} 方法:")
        print(f"  最优解: {result.x}, 函数值: {result.fun}")
    print("\n")
