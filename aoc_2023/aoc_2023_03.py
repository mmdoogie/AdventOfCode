from functools import reduce
from operator import mul
from collections import defaultdict

from mrm.point import adj_diag

with open('data/aoc_2023/03.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse(output = True):
    numbers = {}
    symbols = {}

    for y, d in enumerate(dat):
        num_str = ''
        for x, c in enumerate(d):
            if c in '0123456789':
                num_str += c
            else:
                if num_str != '':
                    numbers[(x - len(num_str), y)] = int(num_str)
                    num_str = ''
                if c != '.':
                    symbols[(x, y)] = c
        if num_str != '':
            numbers[(x - len(num_str), y)] = int(num_str)

    return numbers, symbols

def part1(output = True):
    numbers, symbols = parse(output)

    part_num_sum = 0
    for (x, y), num in numbers.items():
        width = len(str(num))
        adj = set()
        for w in range(width):
            wx = x + w
            adj.update(adj_diag((wx, y)))
        if any(a in symbols for a in adj):
            part_num_sum += num

    return part_num_sum

def part2(output = True):
    numbers, symbols = parse(output)

    gears = defaultdict(set)
    for (x, y), num in numbers.items():
        width = len(str(num))
        adj = set()
        for w in range(width):
            wx = x + w
            adj.update(adj_diag((wx, y)))
        for a in adj:
            if a in symbols and symbols[a] == '*':
                gears[a].add((x, y))

    gear_ratio_sum = 0
    for _, adj in gears.items():
        if len(adj) == 2:
            ratio = reduce(mul, (numbers[a] for a in adj))
            gear_ratio_sum += ratio
        else:
            assert len(adj) == 1

    return gear_ratio_sum

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
