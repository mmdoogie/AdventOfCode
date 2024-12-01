from itertools import combinations
from mrm.util import product

with open('data/aoc_2015/24.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
d = [int(x) for x in dat]

def process(div):
    goal = sum(d) // div
    i = 0
    while True:
        r = []
        for c in combinations(d, i):
            if sum(c) != goal:
                continue
            r += [product(c)]
        if r:
            break
        i += 1
    return min(r)

def part1(output = True):
    return process(3)

def part2(output = True):
    return process(4)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
