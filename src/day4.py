def check_hcl(val):
    if len(val) != 7:
        return False
    if val[0] != "#":
        return False
    return all(map(lambda x: ord("0") <= ord(x) <= ord("9") or ord("a") <= ord(x) <= ord("f"), val[1:]))


def check_hgt(val):
    if "cm" == val[-2:]:
        return 150 <= int(val[:-2]) <= 193
    else:
        return 59 <= int(val[:-2]) <= 76


count1 = 0
count2 = 0
for block in open(0).read().split("\n\n"):
    pw = {}
    for kvp in block.split():
        key, value = kvp.split(":")
        pw[key] = value
    pw.pop("cid", 0)
    if len(pw) != 7:
        continue

    count1 += 1

    byr = pw["byr"]
    iyr = pw["iyr"]
    eyr = pw["eyr"]
    hgt = pw["hgt"]
    hcl = pw["hcl"]
    ecl = pw["ecl"]
    pid = pw["pid"]

    if not (1920 <= int(byr) <= 2002):
        continue
    if not (2010 <= int(iyr) <= 2020):
        continue
    if not (2020 <= int(eyr) <= 2030):
        continue
    if not check_hgt(hgt):
        continue
    if not check_hcl(hcl):
        continue
    if ecl not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        continue
    if not (len(pid) == 9 and all(map(lambda x: x.isdigit(), pid))):
        continue

    count2 += 1


print("Part 1:", count1)
print("Part 2:", count2)
