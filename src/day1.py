def part1(xs, t):
    for i, x1 in enumerate(xs):
        for x2 in xs[i:]:
            if x1 + x2 == t:
                print("Part 1:", x1 * x2)
                return


def part2(xs, t):
    for i1, x1 in enumerate(xs):
        for i2, x2 in enumerate(xs[i1:]):
            if x1 + x2 >= t:
                continue
            for x3 in xs[i1+i2:]:
                if x1 + x2 + x3 == t:
                    print("Part 2:", x1 * x2 * x3)
                    return


xs = list(map(int, open(0).read().splitlines()))
part1(xs, 2020)
part2(xs, 2020)
