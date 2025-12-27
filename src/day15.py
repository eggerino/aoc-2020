starting_numbers = list(map(int, open(0).read().split(",")))
last_occured = {x: i for i, x in enumerate(starting_numbers[:-1])}
previous_number = starting_numbers[-1]

for i in range(len(starting_numbers), 30_000_000):
    if i == 2020:
        print("Part 1:", previous_number)

    if previous_number not in last_occured:
        last_occured[previous_number] = i - 1
        previous_number = 0
    else:
        n = last_occured[previous_number]
        last_occured[previous_number] = i - 1
        previous_number = i - 1 - n

print("Part 2:", previous_number)
