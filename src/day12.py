def apply1(state, inst):
    se, sn, sd = state
    t = inst[0]
    x = int(inst[1:])

    if t == "N":
        return se, sn + x, sd
    if t == "S":
        return se, sn - x, sd
    if t == "E":
        return se + x, sn, sd
    if t == "W":
        return se - x, sn, sd
    if t == "F":
        de, dn = DIRS[sd % 4]
        return se + x * de, sn + x * dn, sd
    if t == "L":
        return se, sn, sd + x // 90
    # if t == "R":
    return se, sn, sd + 4 - (x // 90)


def apply2(state, inst):
    se, sn, we, wn = state
    t = inst[0]
    x = int(inst[1:])

    if t == "N":
        return se, sn, we, wn + x
    if t == "S":
        return se, sn, we, wn - x
    if t == "E":
        return se, sn, we + x, wn
    if t == "W":
        return se, sn, we - x, wn
    if t == "F":
        return se + x * we, sn + x * wn, we, wn
    if inst == "L90" or inst == "R270":
        return se, sn, -wn, we
    if inst == "L180" or inst == "R180":
        return se, sn, -we, -wn
    # if inst == "L270" or inst == "R90":
    return se, sn, wn, -we


instructions = open(0).read().splitlines()
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

state1 = (0, 0, 0)      # east, north, direction
state2 = (0, 0, 10, 1)  # east, north, waypoint-east, waypoint-north

for inst in instructions:
    state1 = apply1(state1, inst)
    state2 = apply2(state2, inst)

print("Part 1:", abs(state1[0]) + abs(state1[1]))
print("Part 2:", abs(state2[0]) + abs(state2[1]))
