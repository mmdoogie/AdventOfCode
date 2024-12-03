from itertools import combinations

with open('data/aoc_2020/09.txt') as f:
    dat = [int(x.strip()) for x in f.readlines()]

def part1(output=False):
    for i, d in enumerate(dat):
        if i < 25:
            continue

        if sum([dat[i-25+a] + dat[i-25+b] == d for a, b in combinations(range(25), 2)]) == 0:
            return d

def part2(output=False):
    p1v = part1(False)
    for a,b in combinations(range(len(dat)), 2):
        if sum(dat[a:b]) == p1v:
            return min(dat[a:b]) + max(dat[a:b])
