adapters = list(map(int, open(0).read().splitlines()))
adapters.append(0)
adapters.sort()
adapters.append(adapters[-1] + 3)


diffs = [adapters[i + 1] - adapters[i] for i in range(len(adapters) - 1)]
print("Part 1:", sum(d == 1 for d in diffs) * sum(d == 3 for d in diffs))


possiblities = [1 for _ in adapters]
for i in range(len(adapters) - 2, -1, -1):
    cur = adapters[i]
    acc = 0
    for i_n in range(i + 1, len(adapters)):
        n = adapters[i_n]
        if n > cur + 3:
            break
        acc += possiblities[i_n]
    possiblities[i] = acc
print("Part 2:", possiblities[0])