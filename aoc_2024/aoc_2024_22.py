from collections import defaultdict
from itertools import pairwise

from mrm.iter import sliding_window

def parse():
    with open('data/aoc_2024/22.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [int(l) for l in lines]

def secret(iv):
    sec = iv
    yield sec
    for _ in range(2000):
        sec = sec * 64 ^ sec
        sec = sec % 16777216
        sec = sec // 32 ^ sec
        sec = sec % 16777216
        sec = sec * 2048 ^ sec
        sec = sec % 16777216
        yield sec

def part1(output=False):
    lines = parse()

    tot = 0
    for l in lines:
        for last in secret(l):
            pass
        tot += last

    return tot

def part2(output=False):
    lines = parse()

    pattern_totals = defaultdict(int)

    for l in lines:
        vals = list(s % 10 for s in secret(l))
        deltas = [b - a for a, b in pairwise(vals)]
        seen = set()
        for i, wind in enumerate(sliding_window(deltas, 4)):
            if wind in seen:
                continue
            pattern_totals[wind] += vals[i + 4]
            seen.add(wind)

    return max(pattern_totals.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
