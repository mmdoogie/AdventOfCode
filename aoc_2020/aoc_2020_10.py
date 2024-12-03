from itertools import pairwise
from functools import cache

with open('data/aoc_2020/10.txt') as f:
    dat = [0] + sorted([int(x.strip()) for x in f.readlines()])
    dat += [max(dat)+3]

def part1(output=False):
    deltas = [j[1]-j[0] for j in pairwise(dat)]
    j1 = sum([d == 1 for d in deltas])
    j3 = sum([d == 3 for d in deltas])
    return j1 * j3

@cache
def tribonacci(x):
    if x == 0:
        return 0
    if x == 1:
        return 0
    if x == 2:
        return 1
    return tribonacci(x - 3) + tribonacci(x - 2) + tribonacci(x - 1)

def part2(output=False):
    deltas = [j[1]-j[0] for j in pairwise(dat)]

    rle = []
    cnt = 0
    lv = deltas[0]
    for d in deltas:
        if lv == d:
            cnt += 1
        else:
            rle += [(lv, cnt)]
            cnt = 1
            lv = d

    tc = 1
    for lv, cnt in rle:
        if lv == 1:
            tc *= tribonacci(cnt + 2)

    return tc
