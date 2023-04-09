import numpy as np
import matplotlib.pyplot as plt

def midpoint_displacement(start, end, roughness, vertical_scale, num_iterations):
    if num_iterations < 1:
        return [start, end]

    mid_x = (start[0] + end[0]) / 2
    displacement = np.random.uniform(-vertical_scale, vertical_scale)
    mid_y = (start[1] + end[1]) / 2 + displacement
    mid_point = (mid_x, mid_y)

    left_points = midpoint_displacement(start, mid_point, roughness, vertical_scale * roughness, num_iterations - 1)
    right_points = midpoint_displacement(mid_point, end, roughness, vertical_scale * roughness, num_iterations - 1)

    return left_points[:-1] + [mid_point] + right_points

start = (0, 0)
end = (1, 0)
roughness = 0.5
vertical_scale = 1
num_iterations = 8

points = midpoint_displacement(start, end, roughness, vertical_scale, num_iterations)
x, y = zip(*points)

plt.plot(x, y)
plt.savefig('fractal_mountain.png')
plt.show()




