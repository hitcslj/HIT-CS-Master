import numpy as np
import matplotlib.pyplot as plt

def julia(c, z, max_iter=1000):
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**4 + c
    return max_iter

def julia_set(c, width=800, height=800, max_iter=1000):
    x_min, x_max = -2, 2
    y_min, y_max = -2, 2
    img = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            zx = x_min + (x_max - x_min) * x / (width - 1)
            zy = y_min + (y_max - y_min) * y / (height - 1)
            z = complex(zx, zy)
            img[y, x] = julia(c, z, max_iter)

    return img

c = complex(-1, 0)
julia_img = julia_set(c)
plt.imshow(julia_img, cmap='twilight_shifted', extent=(-2, 2, -2, 2))
plt.savefig('julia.png')
plt.show()

