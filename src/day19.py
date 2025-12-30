from typing import Dict, List


type Rules = Dict[int, str | List[List[int]]]


def parse_rules(s: str) -> Rules:
    rules = {}
    for line in s.splitlines():
        key, rule = line.split(": ")
        rules[int(key)] = rule[1] if rule.startswith('"') else [[int(num)
                                                                 for num in block.split()] for block in rule.split(" | ")]
    return rules


def match(rules: Rules, s: str, rule_key: int = 0, index: int = 0):
    if index == len(s):
        return []

    rule = rules[rule_key]
    if isinstance(rule, str):
        return [index + 1] if s[index] == rule else []

    matches = []
    for block in rule:
        sub_matches = [index]

        for ref_rule in block:
            new_matches = []
            for idx in sub_matches:
                new_matches += match(rules, s, ref_rule, idx)
            sub_matches = new_matches

        matches += sub_matches

    return matches


rules_str, lines_str = open(0).read().split("\n\n")
rules1 = parse_rules(rules_str)
rules2 = dict(rules1)
rules2[8] = [[42], [42, 8]]
rules2[11] = [[42, 31], [42, 11, 31]]
part1 = 0
part2 = 0
for line in lines_str.splitlines():
    if len(line) in match(rules1, line):
        part1 += 1
    if len(line) in match(rules2, line):
        part2 += 1
print("Part 1:", part1)
print("Part 2:", part2)
