# 图形学实验

这门课是苏老师讲的，选修课，只用交一个实验大作业，题目不限。

自己初步设想，主用python语言，然后使用taichi这个库，来实现一些简单的动画。

参考资料：

- [Taichi官网](https://taichi.graphics/)
- [Taichi中文文档](https://taichi-zh.readthedocs.io/zh_CN/latest/)
- [Taichi中文社区](https://taichi.graphics/cn/)
- [Taichi的视频教程--bilibili](https://space.bilibili.com/490448800/channel/series)
---

偷懒刘，简单记录一下自己的实验大作业的想法：

- [x] 看懂taichi的julia
- [x] 看懂taichi的mandelbrot_zoom动画
- [x] 实现自己的julia_zoom动画
- [x] 如果想要看到更多的动画，可以参考这个[repo](https://github.com/taichi-dev/taichi/tree/master/python/taichi/examples)
要跑上述代码需要安装taichi，可以使用pip安装：
```bash
pip install taichi
```

## 原理说明：

### Julia 集合和 Mandelbrot 集合

Julia 集合和 Mandelbrot 集合是两种著名的分形集合，它们都是在复平面上生成的。分形是一种具有自相似性质的复杂数学结构，即在任意放大倍数下，其形状都会呈现出类似的模式。这两个集合都是通过迭代复数公式生成的，而迭代次数和其收敛性决定了像素点的颜色。

#### Julia 集合

Julia 集合是由这个公式生成的：`Zn+1 = Zn^2 + C`，其中 `Zn` 是复数，`C` 是一个复常数。对于给定的常数 `C`，我们将每个像素点作为初始值 `Z0`，然后对该公式进行迭代。如果在一定迭代次数内，`Zn` 的模（绝对值）保持有界（小于某个阈值，如 2 或 4），那么该点属于 Julia 集合。

#### Mandelbrot 集合

Mandelbrot 集合与 Julia 集合非常相似，但它是在 Julia 集合的基础上引入了一个变化。对于 Mandelbrot 集合，公式为：`Zn+1 = Zn^2 + Cn`，其中 `Cn` 是每次迭代时的复数。在这种情况下，初始值 `Z0` 为 0，`Cn` 等于像素点的位置。这意味着在 Mandelbrot 集合中，每个像素点都对应一个不同的 `Cn` 值。和 Julia 集合一样，如果在一定迭代次数内，`Zn` 的模保持有界，那么该点属于 Mandelbrot 集合。

### 用 Taichi 实现

在 Taichi 实现中，我们用以下步骤渲染 Julia 集合和 Mandelbrot 集合：

1. 初始化：设置画布大小、像素颜色等。
2. 定义颜色函数：根据迭代次数和复数值计算像素颜色。
3. 编写渲染函数：对于每个像素点，进行迭代计算，并设置对应的颜色值。
4. 主循环：在主循环中，调用渲染函数并显示结果。如果需要生成动画效果，可以在循环中改变参数值。

在这两个实现中，主要区别在于迭代公式和参数。在 Julia 集合中，参数 `C` 是一个固定值，而在 Mandelbrot 集合中，参数 `Cn` 随像素位置变化。其他部分，如颜色计算和渲染，基本相同。

### 示例代码

以下是用 Taichi 实现的 Julia 集合和 Mandelbrot 集合的示例代码。

#### Julia 集合

```python
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
        c = ti.Vector([-0.8, ti.cos(t) * 0.2])
        z = ti.Vector([i / n - 1, j / n - 0.5]) * 2
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = 1 - iterations * 0.02


def main():
    gui = ti.GUI("Julia Set", res=(n * 2, n))
    t = 0.0
    while not gui.get_event(ti.GUI.ESCAPE, ti.GUI.EXIT):
        paint(t)
        t += 0.03
        gui.set_image(pixels)
        gui.show()


if __name__ == '__main__':
    main()

```

#### Mandelbrot 集合

```python
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

```

### 结论
Julia 集合和 Mandelbrot 集合是复杂且美丽的分形图像。通过迭代复数公式并在图形中呈现结果，我们可以用 Taichi 这样的高性能计算库轻松地实现它们。这些实现为分形图像的研究、创作和应用提供了一个简单而强大的工具。