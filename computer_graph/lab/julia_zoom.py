import taichi as ti
from taichi.math import cmul, dot, log2, vec2, vec3

ti.init(arch=ti.gpu)

MAXITERS = 100
width, height = 800, 640
pixels = ti.Vector.field(3, ti.f32, shape=(width, height))


@ti.func
def setcolor(z, i):
    v = log2(i + 1 - log2(log2(z.norm()))) / 5
    col = vec3(0.)
    if v < 1.0:
        col = vec3(v**4, v**2.5, v)
    else:
        v = ti.max(0., 2 - v)
        col = vec3(v, v**1.5, v**3)
    return col


@ti.kernel
def render(time: ti.f32):
    zoo = 0.64 + 0.36 * ti.cos(0.02 * time)
    zoo = ti.pow(zoo, 8.0)
    ca = ti.cos(0.15 * (1.0 - zoo) * time)
    sa = ti.sin(0.15 * (1.0 - zoo) * time)
    c = vec2(0.8 * ti.cos(0.1 * time), 0.8 * ti.sin(0.1 * time))
    for i, j in pixels:
        z = 2.0 * vec2(i, j) / height - vec2(1)
        xy = vec2(z.x * ca - z.y * sa, z.x * sa + z.y * ca)
        z = xy * zoo
        count = 0.
        while count < MAXITERS and dot(z, z) < 50:
            z = cmul(z, z) + c
            count += 1.

        if count == MAXITERS:
            pixels[i, j] = [0, 0, 0]
        else:
            pixels[i, j] = setcolor(z, count)


def main():
    gui = ti.GUI("Julia set zoom", res=(width, height))
    for i in range(100000):
        render(i * 0.1)
        gui.set_image(pixels)
        gui.show()


if __name__ == '__main__':
    main()