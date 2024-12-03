from itertools import permutations
from functools import reduce

with open('data/aoc_2020/01.txt') as f:
    dat = [int(x.strip()) for x in f.readlines()]

def doit(cnt):
    for p in permutations(dat, cnt):
        if sum(p) == 2020:
            return reduce(lambda a, b: a*b, p)

def part1(output=False):
    return doit(2)

def part2(output=False):
    return doit(3)
