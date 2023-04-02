import numpy as np


# 目标函数
def f(x):
    return x[0] - x[1] + 2 * x[0] ** 2 + 2 * x[0] * x[1] + x[1] ** 2

# 目标函数的梯度
def gradient_f(x):
    return np.array([1 + 4 * x[0] + 2 * x[1], -1 + 2 * x[0] + 2 * x[1]])

# 精确线搜索找到最优步长
def exact_line_search(x, d):
    alpha = -(d[0]-d[1]+4*x[0]*d[0]+2*x[1]*d[1]+2*d[0]*x[1]+2*d[1]*x[0]) / (4*d[0]**2+2*d[1]**2+4*d[0]*d[1])
    return alpha

def prp_conjugate_gradient(x0, max_iter=100, epsilon=1e-6):
    x = x0
    g = gradient_f(x)
    d = -g
    k = 0
    while k < max_iter:
        g = gradient_f(x)  # 计算梯度
        if np.linalg.norm(g) < epsilon:  # 检查梯度是否满足停止条件
            break
        alpha = exact_line_search(x, d)
        x = x + alpha * d
        g_new = gradient_f(x)
        # 使用Polak-Ribiere方法更新beta
        beta = np.dot(g_new, g_new - g) / np.dot(g, g)
        d = -g_new + beta * d
        g = g_new
        k += 1

    return x, k


x0 = np.array([0, 0])
epsilon = 1e-6
x_min, iterations = prp_conjugate_gradient(x0, max_iter=100,epsilon=epsilon)

print("最小值点：", x_min)
print("最小值：", f(x_min))
print("迭代次数：", iterations)

with open('result_1.txt','w') as file:
    print("最小值点：", x_min,file=file)
    print("最小值：", f(x_min),file=file)
    print("迭代次数：", iterations,file=file)

