def get_any_count(group):
    return len(set(a for p in group.splitlines() for a in p))


def get_all_count(group):
    persons = group.splitlines()
    answers = set(persons[0])
    for p in persons[1:]:
        answers = answers.intersection(p)
    return len(answers)


groups = open(0).read().split("\n\n")
print("Part 1:", sum(map(get_any_count, groups)))
print("Part 2:", sum(map(get_all_count, groups)))
