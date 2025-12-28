from itertools import product


DIRS = list(filter(lambda x: not all(x == 0 for x in x),
            product((-1, 0, 1), repeat=4)))
state = set()
for x, row in enumerate(open(0).read().splitlines()):
    for y, tile in enumerate(row):
        if tile == "#":
            state.add((x, y, 0, 0))
xs = (0, max(x for x, _, _, _ in state))
ys = (0, max(y for _, y, _, _ in state))
zs = (0, 0)
ws = (0, 0)


def apply(state, xs, ys, zs, ws, use_w):
    xmin, xmax = xs
    ymin, ymax = ys
    zmin, zmax = zs
    wmin, wmax = ws

    next_state = set()
    for x in range(xs[0] - 1, xs[1] + 2):
        for y in range(ys[0] - 1, ys[1] + 2):
            for z in range(zs[0] - 1, zs[1] + 2):
                for w in range(ws[0] - 1, ws[1] + 2):

                    if not use_w and w != 0:
                        continue

                    n = sum((x+dx, y+dy, z+dz, w+dw)
                            in state for dx, dy, dz, dw in DIRS)

                    if (x, y, z, w) in state:
                        is_active = n == 2 or n == 3
                    else:
                        is_active = n == 3

                    if is_active:
                        next_state.add((x, y, z, w))
                        xmin, xmax = min(xmin, x), max(xmax, x)
                        ymin, ymax = min(ymin, y), max(ymax, y)
                        zmin, zmax = min(zmin, z), max(zmax, z)
                        wmin, wmax = min(wmin, w), max(wmax, w)

    return next_state, (xmin, xmax), (ymin, ymax), (zmin, zmax), (wmin, wmax)


def run(state, xs, ys, zs, ws, use_w):
    for _ in range(6):
        state, xs, ys, zs, ws = apply(state, xs, ys, zs, ws, use_w)
    return len(state)


print("Part 1:", run(state, xs, ys, zs, ws, False))
print("Part 2:", run(state, xs, ys, zs, ws, True))
