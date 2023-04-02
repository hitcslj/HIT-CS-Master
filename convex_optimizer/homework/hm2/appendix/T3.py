import numpy as np

def f(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2

def grad_f(x):
    return np.array([-400 * x[0] * (x[1] - x[0] ** 2) - 2 * (1 - x[0]), 200 * (x[1] - x[0] ** 2)])

def goldstein(x, d, alpha=1e-4, c1=1e-4, c2=0.9):
    l, r = 0, 1
    while r - l > 1e-6:
        mid = (l + r) / 2
        f1 = f(x + mid * d)
        f2 = f(x) + c1 * mid * np.dot(grad_f(x), d)
        if f1 <= f2:
            r = mid
        else:
            l = mid
    return (l + r) / 2

def goldstein_price(x, d, alpha=1e-4, c1=1e-4, c2=0.9):
    l, r = 0, 1
    while r - l > 1e-6:
        mid = (l + r) / 2
        f1 = f(x + mid * d)
        f2 = f(x) + c1 * mid * np.dot(grad_f(x), d)
        g1 = np.dot(grad_f(x + mid * d), d)
        g2 = c2 * np.dot(grad_f(x), d)
        if f1 <= f2 and g1 >= g2:
            return mid
        elif g1 < g2:
            l = mid
        else:
            r = mid
    return (l + r) / 2

def wolfe_powell(x, d, alpha=1e-4, c1=1e-4, c2=0.9):
    l, r = 0, 1
    while r - l > 1e-6:
        mid = (l + r) / 2
        f1 = f(x + mid * d)
        f2 = f(x) + c1 * mid * np.dot(grad_f(x), d)
        g1 = np.dot(grad_f(x + mid * d), d)
        g2 = c2 * np.dot(grad_f(x), d)
        if f1 <= f2 and abs(g1) <= abs(g2):
            return mid
        elif g1 > 0:
            r = mid
        else:
            l = mid
    return (l + r) / 2

x0 = np.array([-1, 1])
d = np.array([1, 1])

l_goldstein = goldstein(x0, d)
l_goldstein_price = goldstein_price(x0, d)
l_wolfe_powell = wolfe_powell(x0, d)

print("Goldstein方法结果: ", l_goldstein)
print("Goldstein-Price方法结果: ", l_goldstein_price)
print("Wolfe-Powell方法结果: ", l_wolfe_powell)

with open('result_3.txt','w') as f:
    print("Goldstein方法结果: ", l_goldstein,file=f)
    print("Goldstein-Price方法结果: ", l_goldstein_price,file=f)
    print("Wolfe-Powell方法结果: ", l_wolfe_powell,file=f)
