def get_seat(ticket):
    row = 0
    stride = 64
    for d in ticket[:7]:
        if d == "B":
            row += stride
        stride //= 2
    col = 0
    stride = 4
    for d in ticket[7:]:
        if d == "R":
            col += stride
        stride //= 2
    return row, col


def get_id(seat):
    row, col = seat
    return row * 8 + col


ids = set(map(get_id, map(get_seat, open(0).read().splitlines())))
max_id = max(ids)
print("Part 1:", max_id)
for i in range(max_id, 0, -1):
    if i not in ids:
        print("Part 2:", i)
        break
