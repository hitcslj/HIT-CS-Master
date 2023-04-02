import numpy as np

# 目标函数
def f(x):
    return x[0]**2 + 4 * x[1]**2 - 4 * x[0] - 8 * x[1]

# 目标函数的梯度
def gradient_f(x):
    return np.array([2 * x[0] - 4, 8 * x[1] - 8])

# 精确线搜索找到最优步长
def exact_line_search(x, d,epoison=1e-6):
    alpha = -(d[0] * x[0] + 4*d[1] * x[1] -2 *d[0]-4*d[1]) / (d[0]**2 + 4*d[1]**2+epoison)
    return alpha

def bfgs(x0, H, max_iter=10000, epsilon=1e-6):
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

x0 = np.array([0, 0]) # 初始化迭代点
H = np.eye(2)  # 初始化H矩阵为单位阵
x_min, iterations = bfgs(x0,H)

print("最小值点：", x_min)
print("最小值：", f(x_min))
print("迭代次数：", iterations)

with open('result_6.txt','w') as file:
    print("最小值点：", x_min,file=file)
    print("最小值：", f(x_min),file=file)
    print("迭代次数：", iterations,file=file)
