lines = open(0).read().splitlines()
valids1 = 0
valids2 = 0
for line in lines:
    policy, password = line.split(": ")
    r, c = policy.split(" ")
    lower, upper = map(int, r.split("-"))

    count = len(list(filter(lambda x: x == c, password)))
    if lower <= count <= upper:
        valids1 += 1

    if (password[lower - 1] == c) ^ (password[upper - 1] == c):
        valids2 += 1

print("Part 1:", valids1)
print("Part 2:", valids2)
