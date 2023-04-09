import numpy as np
import noise
import matplotlib.pyplot as plt

# 生成Perlin噪声高度图
def generate_height_map(width, height, scale, octaves, persistence, lacunarity):
    height_map = np.zeros((width, height))

    for i in range(width):
        for j in range(height):
            height_map[i][j] = noise.pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence,
                                             lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=42)

    return height_map


# 参数
width = 100
height = 100
scale = 50.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

# 生成高度图
height_map = generate_height_map(width, height, scale, octaves, persistence, lacunarity)

# 创建3D网格
x = np.linspace(0, 1, width)
y = np.linspace(0, 1, height)
x, y = np.meshgrid(x, y)

# 可视化
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, height_map, cmap='terrain', linewidth=0, antialiased=False)
plt.savefig('fractal_mountain_3d.png')
plt.show()

