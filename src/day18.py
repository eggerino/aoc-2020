from typing import Tuple, Literal, List


type Token = int | Literal["+", "*", "(", ")"]
type Node = int | Tuple[Node, Literal["+", "*"], Node]
type Ast = Node


def parse_number(s: str):
    i = 0
    for c in s:
        if not c.isdigit():
            break
        i += 1
    if i != 0:
        num = int(s[:i])
        s = s[i:]
        return num, s


def parse_symbol(symbol: str, s: str):
    if s and s[0] == symbol:
        return symbol, s[1:]


def lex(s: str) -> List[Token]:
    tokens = []
    while s:
        if res := parse_number(s):
            num, s = res
            tokens.append(num)
        elif res := parse_symbol("+", s):
            op, s = res
            tokens.append(op)
        elif res := parse_symbol("*", s):
            op, s = res
            tokens.append(op)
        elif res := parse_symbol("(", s):
            op, s = res
            tokens.append(op)
        elif res := parse_symbol(")", s):
            op, s = res
            tokens.append(op)
        elif res := parse_symbol(" ", s):
            _, s = res
    return tokens


def parse_expr(ts: List[Token], plus_presedence: int = 0, mul_presedence: int = 0) -> Ast:
    presedences = {"+": plus_presedence, "*": mul_presedence}

    def parse_unary() -> Node:
        nonlocal ts

        if not ts:
            return 0

        t = ts[0]
        ts = ts[1:]
        if t == "(":
            return parse_scope()
        return t

    def parse_scope() -> Node:
        nonlocal ts
        node = parse_binary(parse_unary(), 0)
        ts = ts[1:]     # Pop off the closing paren
        return node

    def parse_binary(lhs: Node, min_pres: int) -> Node:
        nonlocal ts, presedences
        while ts and ts[0] in presedences and presedences[ts[0]] >= min_pres:
            op = ts[0]
            ts = ts[1:]
            rhs = parse_unary()

            while ts and ts[0] in presedences and presedences[ts[0]] > min_pres:
                rhs = parse_binary(rhs, presedences[ts[0]])

            lhs = lhs, op, rhs

        return lhs

    return parse_binary(parse_unary(), 0)


def eval_expr(expr: Ast) -> int:
    if isinstance(expr, int):
        return expr

    left, op, right = expr
    left = eval_expr(left)
    right = eval_expr(right)
    if op == "+":
        return left + right
    return left * right


part1 = 0
part2 = 0
for line in open(0).read().splitlines():
    tokens = lex(line)
    part1 += eval_expr(parse_expr(tokens))
    part2 += eval_expr(parse_expr(tokens, plus_presedence=1))

print("Part 1:", part1)
print("Part 2:", part2)
