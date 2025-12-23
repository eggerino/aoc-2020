input = open(0).read()
m1 = list(list(line) for line in input.splitlines())
m2 = list(list(line) for line in input.splitlines())
DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def check_seat(m, r, c):
    if 0 <= r < len(m) and 0 <= c < len(m[r]):
        if m[r][c] == ".":
            return True, False
        return False, m[r][c] == "#"
    else:
        return False, False


def count_neighbors(m, r, c):
    count = 0
    for dr, dc in DIRS:
        i = 1
        is_space, is_taken = True, False
        while is_space:
            is_space, is_taken = check_seat(m, r + dr*i, c + dc*i)
            i += 1
        count += is_taken
    return count


def count_neighbors_single(m, r, c):
    return sum(check_seat(m, r+dr, c+dc)[1] for dr, dc in DIRS)


def apply_round(m, counter, th):
    is_modified = False
    next_m = []
    for r in range(len(m)):
        row = []
        for c in range(len(m[r])):
            t = m[r][c]
            nc = counter(m, r, c)
            if t == "L" and nc == 0:
                is_modified = True
                row.append("#")
            elif t == "#" and nc >= th:
                is_modified = True
                row.append("L")
            else:
                row.append(t)
        next_m.append(row)
    return is_modified, next_m


def count_seats_taken(m):
    return sum(sum(t == "#" for t in r) for r in m)


def print_seats(m):
    for row in m:
        print("".join(row))


while True:
    is_modified, m1 = apply_round(m1, count_neighbors_single, 4)
    if not is_modified:
        break
print(count_seats_taken(m1))

while True:
    is_modified, m2 = apply_round(m2, count_neighbors, 5)
    if not is_modified:
        break
print(count_seats_taken(m2))
