import numpy as np

def f(x):
    return x[0] - x[1] + 2 * x[0] ** 2 + 2 * x[0] * x[1] + x[1] ** 2

def gradient(x):
    df_dx1 = 1 + 4 * x[0] + 2 * x[1]
    df_dx2 = -1 + 2 * x[0] + 2 * x[1]
    return np.array([df_dx1, df_dx2])

def conjugate_gradient(x0, epsilon):
    x = x0
    r = -gradient(x)
    d = r
    k = 0

    while np.linalg.norm(r) > epsilon:
        alpha = np.dot(r, r) / np.dot(d, gradient(x + d))
        x = x + alpha * d
        r_new = r - alpha * gradient(x)
        beta = np.dot(r_new, r_new) / np.dot(r, r)
        d = r_new + beta * d
        r = r_new
        k += 1

    return x, k

x0 = np.array([0, 0])
epsilon = 1e-6
x_min, iterations = conjugate_gradient(x0, epsilon)

print("最小值点：", x_min)
print("迭代次数：", iterations)
