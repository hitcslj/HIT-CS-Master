import turtle
import matplotlib.pyplot as plt
import numpy as np

# 计算Bezier曲线上的点
def bezier_curve(points, t):
    n = len(points) - 1
    b = np.zeros((n+1, len(t)))
    for i in range(n+1):
        b[i, :] = comb(n, i) * t**i * (1-t)**(n-i)

    x = np.dot(points[:, 0],b)
    y = np.dot(points[:, 1],b)
    return x, y

# 计算组合数
def comb(n, i):
    return np.math.factorial(n) / (np.math.factorial(i) * np.math.factorial(n-i))

# 设定控制点坐标
points = np.array([[-100, 0], [0, 100], [100,0]])

# 计算Bezier曲线上的点
t = np.linspace(0, 1, 10)
x, y = bezier_curve(points, t)

# 使用turtle模块绘制Bezier曲线
turtle.speed(1)
turtle.pensize(5)
turtle.penup()
turtle.goto(points[0][0], points[0][1])
turtle.pendown()
for i in range(len(x)):
    turtle.goto(x[i], y[i])
turtle.done()

# 使用matplotlib库绘制Bezier曲线并标明控制点
plt.plot(x, y, 'b-', label='Bezier Curve')
plt.plot(points[:, 0], points[:, 1], 'ro', label='Control Points')
plt.legend()
plt.savefig('bezier.png')
plt.show()