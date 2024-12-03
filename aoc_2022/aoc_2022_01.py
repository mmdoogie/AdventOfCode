from itertools import groupby

def parse():
    with open('data/aoc_2022/01.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()
    cal = []
    for k, items in groupby(lines, key=lambda x: len(x) > 0):
        if not k:
            continue
        cal += [sum(int(i) for i in items)]
    return max(cal)

def part2(output=False):
    lines = parse()
    cal = []
    for k, items in groupby(lines, key=lambda x: len(x) > 0):
        if not k:
            continue
        cal += [sum(int(i) for i in items)]
    return sum(sorted(cal, reverse=True)[0:3])
