import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def lorenz_system(t, state, sigma, rho, beta):
    x, y, z = state
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]

# 设置Lorenz方程的参数
sigma = 10
rho = 28
beta = 8/3

# 设置初始条件
initial_state = [1, 1, 1]

# 设置时间范围
t_span = (0, 50)
t_eval = np.linspace(t_span[0], t_span[1], 10000)

# 解Lorenz方程
solution = solve_ivp(lorenz_system, t_span, initial_state, t_eval=t_eval, args=(sigma, rho, beta))
x, y, z = solution.y

# 绘制Lorenz吸引子
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Lorenz Attractor')
plt.savefig('Lorenz.png')
plt.show()

