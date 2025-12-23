import math

g = open(0).read().splitlines()
slopes = [(3, 1), (1, 1), (5, 1), (7, 1), (1, 2)]
counts = []
for dc, dr in slopes:
    count = 0
    ir = 0
    ic = 0
    while ir < len(g):
        ic %= len(g[ir])
        if g[ir][ic] == "#":
            count += 1
        ir += dr
        ic += dc
    counts.append(count)

print("Part 1:", counts[0])
print("Part 2:", math.prod(counts))
