import numpy as np

# 目标函数
def f(x):
    return 10 * x[0]**2 + x[1]**2

# 目标函数的梯度
def gradient_f(x):
    return np.array([20 * x[0], 2 * x[1]])

# 精确线搜索找到最优步长
def exact_line_search(x, d):
    alpha = -(10 * x[0] * d[0] + x[1] * d[1]) / (10 * d[0]**2 + d[1]**2)
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

    return x, k

x0 = np.array([0.1, 1]) # 初始化迭代点
H = np.eye(2)  # 初始化H矩阵为单位阵

x_min, iterations = dfp(x0,H)
print("最小值点：", x_min)
print("最小值：", f(x_min))
print("迭代次数：", iterations)

with open('result_5.txt','w') as file:
    print("最小值点：", x_min,file=file)
    print("最小值：", f(x_min),file=file)
    print("迭代次数：", iterations,file=file)
