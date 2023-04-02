# import numpy as np
from scipy.optimize import minimize
import autograd.numpy as np
from autograd import grad

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

# Ackley函数
def ackley(x):
    # 全局极小值在原点
    a, b, c = 20, 0.2, 2 * np.pi
    return -a * np.exp(-b * np.sqrt((x[0]**2 + x[1]**2) / 2)) - np.exp((np.cos(c * x[0]) + np.cos(c * x[1])) / 2) + a + np.exp(1)

# Booth函数
def booth(x):
    # 极小值在（1，3）,最优值为0
    return (x[0] + 2 * x[1] - 7)**2 + (2 * x[0] + x[1] - 5)**2

# Branin函数
def branin(x):
    # 极小值在（-pi，12.275），（pi，2.275），（9.42478，2.475）
    a, b, c, r, s, t = 1, 5.1 / (4 * np.pi**2), 5 / np.pi, 6, 10, 1 / (8 * np.pi)
    return a * (x[1] - b * x[0]**2 + c * x[0] - r)**2 + s * (1 - t) * np.cos(x[0]) + s

# Flower函数
def flower(x):
    # 最小值靠近原点，但不是原点
    a,b,c = 1,1,4

    return a*np.sqrt(x[0]**2+x[1]**2)+b*np.sin(c*np.arctan2(x[1],x[0]))

# Michalewicz函数
def michalewicz(x):
    # 二维函数，全局最小值为-1.8013，最优解为（2.20，1.57）
    m = 10
    return -np.sum(np.sin(x) * np.sin((x**2) / np.pi)**(2 * m))

# Rosenbrock Banana函数
def rosenbrock_banana(x):
    # 极小值在（a，a**2），最优值为0
    a, b = 1, 5
    return (a - x[0])**2 - b*(x[1] - x[0]**2)**2

# Wheeler函数
def wheeler(x):
    # 全局最小值在（1，-2/3），最优值为-1
    a = 1.5
    return -np.exp(-(x[0]*x[1]-a)**2-(x[1]-a)**2)

def plot_function(func, func_name, x_range, y_range):
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.array([func(np.array([x, y])) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = Z.reshape(X.shape)

    # Contour plot
    plt.figure()
    contour = plt.contour(X, Y, Z)
    plt.clabel(contour, inline=True, fontsize=8)
    plt.title(f"{func_name} - Contour plot")
    plt.xlabel("x")
    plt.ylabel("y")

    # 3D surface plot
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title(f"{func_name} - 3D Surface plot")
    plt.show()

# Define the range of x and y values
x_range = np.linspace(-5, 5, 100)
y_range = np.linspace(-5, 5, 100)

# Plot the functions
# plot_function(ackley, "Ackley", x_range, y_range)
# plot_function(booth, "Booth", x_range, y_range)
# plot_function(branin, "Branin", x_range, y_range)
plot_function(flower, "Flower", x_range, y_range)
# plot_function(michalewicz, "Michalewicz", x_range, y_range)
# plot_function(rosenbrock_banana, "Rosenbrock Banana", x_range, y_range)
# plot_function(wheeler, "Wheeler", x_range, y_range)


# Initial guess for the starting point
initial_guess = np.array([0.99, 0.99])
print(rosenbrock_banana(initial_guess))


# Function names and their corresponding functions
functions = {
    "Ackley": ackley,
    "Booth": booth,
    "Branin": branin,
    "Flower": flower,
    "Michalewicz": michalewicz,
    "Rosenbrock Banana": rosenbrock_banana,
    "Wheeler": wheeler
}

# Function-specific initial guesses
initial_guesses = {
    "Ackley": np.array([0.0, 0.0]),
    "Booth": np.array([1.0, 3.0]),
    "Branin": np.array([-3.0, 12.0]),
    "Flower": np.array([0.0, 0.0]),
    "Michalewicz": np.array([2.20, 1.57]),
    "Rosenbrock Banana": np.array([1.0, 1.0]),
    "Wheeler": np.array([1.0, -2/3])
}

# Function-specific bounds
bounds = {
    "Ackley": [(-5.0, 5.0), (-5.0, 5.0)],
    "Booth": [(-10.0, 10.0), (-10.0, 10.0)],
    "Branin": [(-5.0, 10.0), (0.0, 15.0)],
    "Flower": [(-2.0, 2.0), (-2.0, 2.0)],
    "Michalewicz": [(0.0, 3.0), (0.0, 3.0)],
    "Rosenbrock Banana": [(-5.0, 5.0), (-5.0, 5.0)],
    "Wheeler": [(-5.0, 5.0), (-5.0, 5.0)]
}

# Find the minimum values of the functions using the L-BFGS-B method
with open("result.txt", "w") as result_file:
    for func_name, func in functions.items():
        initial_guess = initial_guesses[func_name]
        bound = bounds[func_name]
        gradient = grad(func)
        result = minimize(func, initial_guess, method="BFGS", bounds=bound, jac=gradient, options={"maxiter": 10000, "disp": True})
        output = f"{func_name} - Minimum value: {result.fun} at {result.x}\n"
        print(output)
        result_file.write(output)
