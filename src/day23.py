def parse_cups(s: str, part2: bool):
    nums = list(map(int, s))
    cups = dict(zip(nums, nums[1:]))
    if part2:
        cups[nums[-1]] = 10
        cups[1_000_000] = nums[0]
        for i in range(10, 1_000_000):
            cups[i] = i + 1
    else:
        cups[nums[-1]] = nums[0]
    return cups, nums[0]


def play_round(cups: dict[int, int], cur: int, part2: bool):
    c = cur
    pick_up = [(c := cups[c]) for _ in range(3)]

    dest = get_dest(cur, pick_up, part2)

    cups[cur] = cups[pick_up[-1]]
    cups[pick_up[-1]] = cups[dest]
    cups[dest] = pick_up[0]

    return cups[cur]


def get_dest(cur: int, pick_up: list[int], part2: bool):
    max_label = 1_000_000 if part2 else 9
    cur = cur - 1 if cur > 1 else max_label
    while cur in pick_up:
        cur = cur - 1 if cur > 1 else max_label
    return cur


def get_result_part1(cups: dict[int, int]):
    nums = []
    c = cups[1]
    while c != 1:
        nums.append(c)
        c = cups[c]
    return "".join(map(str, nums))


def get_result_part2(cups: dict[int, int]):
    c = cups[1]
    return c * cups[c]


data = open(0).read()
for part2 in [False, True]:
    cups, cur = parse_cups(data, part2)

    for _ in range(10_000_000 if part2 else 100):
        cur = play_round(cups, cur, part2)

    result = get_result_part2(cups) if part2 else get_result_part1(cups)

    part_str = "Part 2:" if part2 else "Part 1:"
    print(part_str, result)
