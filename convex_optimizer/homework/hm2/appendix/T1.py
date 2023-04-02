import numpy as np

def f(x):
    return x[0] - x[1] + 2 * x[0] ** 2 + 2 * x[0] * x[1] + x[1] ** 2

def gradient(x):
    df_dx1 = 1 + 4 * x[0] + 2 * x[1]
    df_dx2 = -1 + 2 * x[0] + 2 * x[1]
    return np.array([df_dx1, df_dx2])

def hessian(x):
    d2f_dx11 = 4
    d2f_dx21 = 2
    d2f_dx12 = 2
    d2f_dx22 = 2
    return np.array([[d2f_dx11, d2f_dx12], [d2f_dx21, d2f_dx22]])

def fr_pr_conjugate_gradient(x0, epsilon):
    x = x0
    r = gradient(x)
    d = -r
    k = 0
    A = hessian(x)
    while np.linalg.norm(r) > epsilon:
        alpha = -np.dot(r, d) / np.dot(d, np.dot(A, d)) # 使用Fletcher-Reeves方法更新alpha
        x = x + alpha * d
        r_new = gradient(x)

        # 使用Polak-Ribiere方法更新beta
        beta = np.dot(r_new, r_new - r) / np.dot(r, r)

        d = -r_new + beta * d
        r = r_new
        k += 1

    return x, k


x0 = np.array([0, 0])
epsilon = 1e-6
x_min, iterations = fr_pr_conjugate_gradient(x0, epsilon)

print("最小值点：", x_min)
print("最小值：", f(x_min))
print("迭代次数：", iterations)