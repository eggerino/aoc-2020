def parse_rule(rule: str):
    src, targets = rule.split(" bags contain ")
    ts = {}
    for target in targets.split(", "):
        number, color = target.split(" ", 1)
        if number == "no":
            continue
        color = color.split(" bag", 1)[0]
        ts[color] = int(number)
    return src, ts


def find_all(bag, collector: set):
    for target in inverted_rules[bag]:
        if target in collector:
            continue
        collector.add(target)
        find_all(target, collector)
    return collector


def get_inside_count(bag):
    if not rules[bag]:
        return 0

    count = 0
    for t, n in rules[bag].items():
        count += n * (1 + get_inside_count(t))
    return count


rules = dict(map(parse_rule, open(0).read().splitlines()))
inverted_rules = dict(map(lambda x: (x, []), rules))
for src, ts in rules.items():
    for t in ts:
        inverted_rules[t].append(src)

print("Part 1:", len(find_all("shiny gold", set())))
print("Part 2:", get_inside_count("shiny gold"))
