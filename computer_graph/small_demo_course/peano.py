import matplotlib.pyplot as plt


def peano_curve(level, dx, dy):
    if level == 0:
        return [(0, 0), (0, dy), (dx, dy), (dx, 0)]
    else:
        next_level = level - 1
        third_dx = dx / 3.0
        third_dy = dy / 3.0
        pts = []

        for x_offset, y_offset, x_mult, y_mult in [
            (0, 0, 1, 1),
            (0, third_dy, 1, -1),
            (0, 2 * third_dy, 1, 1),
            (third_dx, 2 * third_dy, -1, 1),
            (third_dx, third_dy, -1, -1),
            (third_dx, 0, -1, 1),
            (2 * third_dx, 0, 1, 1),
            (2 * third_dx, third_dy, 1, -1),
            (2 * third_dx, 2 * third_dy, 1, 1),
        ]:
            for x, y in peano_curve(next_level, x_mult * third_dx, y_mult * third_dy):
                pts.append((x + x_offset, y + y_offset))
        return pts


level = 3
curve_points = peano_curve(level, 1, 1)

x, y = zip(*curve_points)
plt.plot(x, y, "b-")
plt.axis("scaled")
plt.axis("off")
plt.savefig('peano.png')
plt.show()

