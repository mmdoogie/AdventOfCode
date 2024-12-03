from collections import deque

with open('data/aoc_2020/22.txt') as f:
    dat = [x.strip() for x in f.readlines()]

deck1 = deque()
deck2 = deque()
for d in dat:
    if ':' in d:
        if d[-2] == '1':
            activeDeck = deck1
        else:
            activeDeck = deck2
        continue
    if d == '':
        continue
    activeDeck.append(int(d))

def compute_part1(deck1, deck2):
    while len(deck1) > 0 and len(deck2) > 0:
        c1 = deck1.popleft()
        c2 = deck2.popleft()
        if c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)

    if len(deck1) > 0:
        winner = deck1
    else:
        winner = deck2

    score = sum([(i+1) * c for i, c in enumerate(reversed(winner))])
    return score

def part1(output=False):
    return compute_part1(deque(deck1), deque(deck2))

def compute_part2(deck1, deck2):
    seenRounds = []

    while len(deck1) > 0 and len(deck2) > 0:
        rid = ','.join([str(x) for x in deck1]) + ';' + ','.join([str(x) for x in deck2])
        if rid in seenRounds:
            return 1
        seenRounds += [rid]
        c1 = deck1.popleft()
        c2 = deck2.popleft()
        if c1 <= len(deck1) and c2 <= len(deck2):
            winner = compute_part2(deque(list(deck1)[:c1]), deque(list(deck2)[:c2]))
            if winner == 1:
                deck1.append(c1)
                deck1.append(c2)
            else:
                deck2.append(c2)
                deck2.append(c1)
        else:
            if c1 > c2:
                deck1.append(c1)
                deck1.append(c2)
            else:
                deck2.append(c2)
                deck2.append(c1)
    if len(deck1) > 0:
        return 1
    else:
        return 2

def part2(output=False):
    p2d1 = deque(deck1)
    p2d2 = deque(deck2)
    if compute_part2(p2d1, p2d2) == 1:
        winner = p2d1
    else:
        winner = p2d2
    score = sum([(i+1) * c for i, c in enumerate(reversed(winner))])
    return score
