import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter=1000):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**2 + c
    return max_iter

def mandelbrot_set(width=800, height=800, max_iter=1000):
    x_min, x_max = -2, 1
    y_min, y_max = -1.5, 1.5
    img = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            cx = x_min + (x_max - x_min) * x / (width - 1)
            cy = y_min + (y_max - y_min) * y / (height - 1)
            c = complex(cx, cy)
            img[y, x] = mandelbrot(c, max_iter)

    return img

mandelbrot_img = mandelbrot_set()
plt.imshow(mandelbrot_img, cmap='twilight_shifted', extent=(-2, 1, -1.5, 1.5))
plt.savefig('mandelbrot.png')
plt.show()


