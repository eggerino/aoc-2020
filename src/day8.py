def parse_inst(line: str):
    inst, op = line.split()
    return inst, int(op)


def evaluate_prog(prog):
    acc = 0
    ip = 0
    inst_visited = set()
    while ip < len(prog):
        if ip in inst_visited:
            return acc, False
        inst_visited.add(ip)

        inst, op = prog[ip]
        if inst == "nop":
            ip += 1
        elif inst == "acc":
            acc += op
            ip += 1
        else:   # jmp
            ip += op

    return acc, True


prog = list(map(parse_inst, open(0).read().splitlines()))
print("Part 1:", evaluate_prog(prog)[0])

for i in range(len(prog)):
    inst, op = prog[i]
    if inst == "nop":
        prog[i] = ("jmp", op)
    elif inst == "jmp":
        prog[i] = ("nop", op)
    else:
        continue

    acc, terminated = evaluate_prog(prog)
    prog[i] = (inst, op)
    if terminated:
        print("Part 2:", acc)
        break
