start, ids = open(0).read().splitlines()
start = int(start)
ids = list(map(lambda x: (x[0], int(x[1])), filter(
    lambda x: x[1] != "x", enumerate(ids.split(",")))))

part1 = min(map(lambda id: (id - start % id, id), map(lambda x: x[1], ids)))
print("Part 1:", part1[0] * part1[1])


part2 = 1
mode = 1
for i, x in ids:
    while (part2 + i) % x != 0:
        part2 += mode
    mode *= x
print("Part 2:", part2)
