from collections import deque


def parse_range(s: str):
    start, end_inclusive = map(int, s.split("-"))
    return range(start, end_inclusive + 1)


def parse_rule(s: str):
    name, value = s.split(": ")
    return name, tuple(map(parse_range, value.split(" or ")))


def parse_ticket(s: str):
    return [*map(int, s.split(","))]


def filter_invalid_tickets(ts: list[list[int]]):
    error_rate = 0
    valids = []
    for t in ts:
        is_valid = True
        for field in t:
            if all(field not in r1 and field not in r2 for r1, r2 in rules.values()):
                error_rate += field
                is_valid = False
                break
        if is_valid:
            valids.append(t)
    return error_rate, valids


def find_rule_names(valids: list[list[int]]):
    valids = list(zip(*valids))  # transponse
    q = deque(rules.items())
    names = ["" for _ in valids]
    while q:
        name, (r1, r2) = q.popleft()

        last_match = 0
        matches = 0
        for i, fields in enumerate(valids):
            if names[i]:
                continue    # Already taken

            if all(field in r1 or field in r2 for field in fields):
                matches += 1
                last_match = i

        if matches == 1:
            # Found an exact match -> must be the rule
            names[last_match] = name
        else:
            # rules is still ambigous -> try other rules next befor resuming to this one
            q.append((name, (r1, r2)))

    return names


rules_str, my_ticket_str, other_tickets_str = open(0).read().split("\n\n")
rules = dict(map(parse_rule, rules_str.splitlines()))
my_ticket = parse_ticket(my_ticket_str.splitlines()[1])
other_tickets = map(parse_ticket, other_tickets_str.splitlines()[1:])

part1, valid_tickets = filter_invalid_tickets(other_tickets)
print("Part 1:", part1)

valid_tickets.append(my_ticket)
names = find_rule_names(valid_tickets)
part2 = 1
for name, field in zip(names, my_ticket):
    if name.startswith("departure"):
        part2 *= field
print("Part 2:", part2)
