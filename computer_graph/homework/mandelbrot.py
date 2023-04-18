import taichi as ti

ti.init(arch=ti.gpu)

n = 320
pixels = ti.field(dtype=float, shape=(n * 2, n))


@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])


@ti.kernel
def paint(t: float):
    for i, j in pixels:  # Parallelized over all pixels
        c = ti.Vector([(i / n - 1.5) * 2, (j / n - 0.5) * 2])
        z = ti.Vector([ti.sin(t)*0.2, ti.cos(t) * 0.2]) # 制作动画效果，对于一个mandelbrot集，z的值是不变的.
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = 1 - iterations * 0.02


def main():
    gui = ti.GUI("Mandelbrot Set", res=(n * 2, n))
    t = 0.0
    while not gui.get_event(ti.GUI.ESCAPE, ti.GUI.EXIT):
        paint(t)
        t += 0.01
        gui.set_image(pixels)
        gui.show()


if __name__ == '__main__':
    main()
