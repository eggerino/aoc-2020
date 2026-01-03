from collections import deque


def parse_deck(s: str):
    return tuple(map(int, s.splitlines()[1:]))


def play_combat(p1: tuple[int, ...], p2: tuple[int, ...]):
    p1 = deque(p1)
    p2 = deque(p2)
    while p1 and p2:
        c1 = p1.popleft()
        c2 = p2.popleft()
        if c1 > c2:
            p1.extend((c1, c2))
        else:
            p2.extend((c2, c1))
    if p1:
        return 1, tuple(p1)
    else:
        return 2, tuple(p2)


def play_rec_combat(p1: tuple[int, ...], p2: tuple[int, ...]):
    def play(p1: tuple[int, ...], p2: tuple[int, ...]):
        seen = set()
        while p1 and p2:
            if (p1, p2) in seen:
                return 1, p1
            seen.add((p1, p2))

            c1, p1 = p1[0], p1[1:]
            c2, p2 = p2[0], p2[1:]

            if c1 <= len(p1) and c2 <= len(p2):
                winner, _ = play(p1[:c1], p2[:c2])
            else:
                winner = 1 if c1 > c2 else 2

            if winner == 1:
                p1 = *p1, c1, c2
            else:
                p2 = *p2, c2, c1

        if p1:
            return 1, p1
        else:
            return 2, p2

    return play(p1, p2)


def compute_score(deck: tuple[int, ...]):
    return sum(card * (i + 1) for i, card in enumerate(reversed(deck)))


p1, p2 = map(parse_deck, open(0).read().split("\n\n"))
print("Part 1:", compute_score(play_combat(p1, p2)[1]))
print("Part 2:", compute_score(play_rec_combat(p1, p2)[1]))
