prog = open(0).read().splitlines()
memory_v1 = {}
memory_v2 = {}
mask_0 = []
mask_1 = []
mask_X = []


def eval_mask(inst: str):
    mask = inst.split(" = ")[1]
    mask_0.clear()
    mask_1.clear()
    mask_X.clear()
    for i, x in enumerate(reversed(mask)):
        if x == "1":
            mask_1.append(i)
        elif x == "0":
            mask_0.append(i)
        else:
            mask_X.append(i)


def set_bit(val, i):
    return val | (1 << i)


def clear_bit(val, i):
    return val & ~(1 << i)


def eval_mem_v1(inst: str):
    addr = int(inst.split("[")[1].split("]")[0])
    val = int(inst.split(" = ")[1])

    for i in mask_1:
        val = set_bit(val, i)
    for i in mask_0:
        val = clear_bit(val, i)
    memory_v1[addr] = val


def eval_mem_v2(inst: str):
    addr = int(inst.split("[")[1].split("]")[0])
    val = int(inst.split(" = ")[1])

    for i in mask_1:
        addr = set_bit(addr, i)

    for a in get_all_addrs(addr):
        memory_v2[a] = val


def get_all_addrs(addr):
    # start with all 0 in x pos
    for i in mask_X:
        addr = clear_bit(addr, i)

    n_addrs = 2**len(mask_X)
    addrs = [addr for i in range(n_addrs)]
    for i_addr in range(n_addrs):
        for i_x, x in enumerate(mask_X):
            p = 2**(i_x + 1)
            if (i_addr % p) < (p // 2):
                addrs[i_addr] = set_bit(addrs[i_addr], x)
    return addrs


for inst in prog:
    if inst.startswith("mask = "):
        eval_mask(inst)
    else:
        eval_mem_v1(inst)
        eval_mem_v2(inst)

print("Part 1:", sum(memory_v1.values()))
print("Part 2:", sum(memory_v2.values()))
