def is_valid(idx):
    num = nums[idx]
    prev = nums[idx-preample_length:idx]
    for i, n1 in enumerate(prev):
        for n2 in prev[i + 1:]:
            if n1 + n2 == num:
                return True
    return False


def get_first_invalid_idx():
    for i in range(preample_length, len(nums)):
        if not is_valid(i):
            return i


def get_first_range_summed(num):
    for i_lower in range(len(nums)):
        acc = nums[i_lower]
        for i_upper in range(i_lower + 1, len(nums)):
            if acc == num:
                return i_lower, i_upper
            if acc > num:
                break
            acc += nums[i_upper]


nums = list(map(int, open(0).read().splitlines()))
preample_length = 25
invalid_num = nums[get_first_invalid_idx()]
i_lower, i_upper = get_first_range_summed(invalid_num)
print("Part 1:", invalid_num)
print("Part 2:", min(nums[i_lower:i_upper]) + max(nums[i_lower:i_upper]))
