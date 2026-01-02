def parse_image(s: str):
    header, *image = s.splitlines()
    id = int(header.split()[1].split(":")[0])
    borders = [], [], [], []
    n = len(image)
    for i in range(n):
        borders[0].append(True if image[0][i] == "#" else False)
        borders[1].append(True if image[-1][i] == "#" else False)
        borders[2].append(True if image[i][0] == "#" else False)
        borders[3].append(True if image[i][-1] == "#" else False)
    return id, borders


def match_border(first, second):
    return all(f == s for f, s in zip(first, second)) or all(f == s for f, s in zip(first, reversed(second)))


images = [parse_image(d) for d in open(0).read().split("\n\n")]

result = 1
for id, borders in images:
    matches = 0
    for border in borders:
        for other_id, other_borders in images:
            if id == other_id:
                continue
            for other_border in other_borders:
                if match_border(border, other_border):
                    matches += 1

    if matches == 2:
        result *= id

print("Part 1:", result)
