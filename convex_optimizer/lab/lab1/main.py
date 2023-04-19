import numpy as np
from scipy.optimize import minimize

import numpy as np


# 目标函数
def f(x):
    return x[0] - x[1] + 2 * x[0] ** 2 + 2 * x[0] * x[1] + x[1] ** 2

# 目标函数的梯度
def gradient_f(x):
    return np.array([1 + 4 * x[0] + 2 * x[1], -1 + 2 * x[0] + 2 * x[1]])

# 目标函数的Hessian矩阵
def hessian(x):
    return np.array([[4, 2], [2, 2]])

# 精确线搜索找到最优步长
def exact_line_search(x, d):
    alpha = -(d[0]-d[1]+4*x[0]*d[0]+2*x[1]*d[1]+2*d[0]*x[1]+2*d[1]*x[0]) / (4*d[0]**2+2*d[1]**2+4*d[0]*d[1])
    return alpha


# 使用DFP方法求解
def dfp(x0, H, max_iter=100, epsilon=1e-6):
    x = x0
    H = H
    k = 0

    while k < max_iter:
        g = gradient_f(x)  # 计算梯度
        if np.linalg.norm(g) < epsilon:  # 检查梯度是否满足停止条件
            break

        d = -H.dot(g)  # 计算搜索方向
        alpha = exact_line_search(x, d)  # 精确线搜索找到最优步长
        x_next = x + alpha * d  # 更新迭代点

        delta_x = x_next - x
        delta_g = gradient_f(x_next) - g

        H = H + np.outer(delta_x, delta_x) / delta_x.dot(delta_g) - (H.dot(np.outer(delta_g, delta_g)).dot(H)) / (delta_g.dot(H).dot(delta_g))

        x = x_next
        k += 1
    return x,k

def bfgs(x0, H=np.exp(2), max_iter=10000, epsilon=1e-6):
    x = x0
    k = 0

    while k < max_iter:
        g = gradient_f(x)  # 计算梯度
        if np.linalg.norm(g) < epsilon:  # 检查梯度是否满足停止条件
            break

        d = -H.dot(g)  # 计算搜索方向
        alpha = exact_line_search(x, d)  # 精确线搜索找到最优步长
        x_next = x + alpha * d  # 更新迭代点

        delta_x = x_next - x # p
        delta_g = gradient_f(x_next) - g # q

        Hg = H.dot(delta_g)
        term1 = (1 + delta_g.T.dot(Hg) / delta_x.dot(delta_g)) * np.outer(delta_x, delta_x) / delta_x.dot(delta_g)
        term2 = (np.outer(delta_x, delta_g).dot(H) + np.outer(Hg, delta_x)) / delta_x.dot(delta_g)
        H = H + term1 - term2

        x = x_next
        k += 1

    return x, k

def fr(x0, H=np.eye(2),max_iter=100, epsilon=1e-6):
    x = x0
    g = gradient_f(x)
    H = hessian(x)
    d = -g
    k = 0
    while k < max_iter:
        g = gradient_f(x)  # 计算梯度
        if np.linalg.norm(g) < epsilon:  # 检查梯度是否满足停止条件
            break
        alpha = -g.T.dot(d) / d.T.dot(H).dot(d)
        x = x + alpha * d
        g_new = gradient_f(x)
        # 使用Polak-Ribiere方法更新beta
        beta = d.T.dot(H).dot(g_new) / d.T.dot(H).dot(d)
        d = -g_new + beta * d
        g = g_new
        k += 1

    return x, k



# 梯度下降方法
def gradient_descent(x0,H, max_iter=10000, epsilon=1e-6):
    x = x0
    k = 0
    while k < max_iter:
        g = gradient_f(x)
        if np.linalg.norm(g) < epsilon:
            break
        x = x - 0.01 * g
        k += 1
    return x, k

# 牛顿法
def newton_method(x0, H,max_iter=10000, epsilon=1e-6):
    x = x0
    k = 0
    while k < max_iter:
        g = gradient_f(x)
        if np.linalg.norm(g) < epsilon:
            break
        H = hessian(x)
        x = x - np.linalg.inv(H).dot(g)
        k += 1
    return x, k

# Nelder-Mead方法（无导数）
def nelder_mead(x0, H,max_iter=10000, epsilon=1e-6):
    res = minimize(f, x0, method='nelder-mead', options={'xatol': epsilon, 'maxiter': max_iter})
    return res.x, res.nit

x0 = np.array([0, 0])
H = np.eye(2)
epsilon = 1e-6

methods = {
    "DFP": dfp,
    "BFGS": bfgs,
    "FR": fr,
    "Gradient Descent": gradient_descent,
    "Newton": newton_method,
    "Nelder-Mead": nelder_mead
}

# 使用不同的方法找到函数的最小值
with open("result.txt", "w") as file:
    for method_name, method in methods.items():
        x_min, iterations = method(x0, H,max_iter=10000, epsilon=epsilon)
        x_min = np.round(x_min, 2)
        y_min = np.round(f(x_min), 2)
        output = f"{method_name} - Minimum value: {y_min} at {x_min} - iterations : {iterations}\n"
        print(output)
        print(output, file=file)
