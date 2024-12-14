from collections import Counter
from functools import reduce
import operator

import mrm.image as img
from mrm.parse import all_nums
import mrm.point as pt

def parse():
    with open('data/aoc_2024/14.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    robots = [tuple(all_nums(l)) for l in lines]
    return robots

WIDTH = 101
HEIGHT = 103

def part1(output=False):
    robots = parse()

    sec = 100
    at_end = [((r[0] + sec * r[2]) % WIDTH, (r[1] + sec * r[3]) % HEIGHT) for r in robots]

    def quad(r):
        if r[0] < WIDTH // 2:
            if r[1] < HEIGHT // 2:
                return 1
            if r[1] > HEIGHT // 2:
                return 2
        if r[0] > WIDTH // 2:
            if r[1] < HEIGHT // 2:
                return 3
            if r[1] > HEIGHT // 2:
                return 4
        return 0

    qcnt = Counter(quad(r) for r in at_end)
    return reduce(operator.mul, (v for k, v in qcnt.items() if k != 0))

def part2(output=False):
    robots = parse()

    sec = 1
    while True:
        at_end = [((r[0] + sec * r[2]) % WIDTH, (r[1] + sec * r[3]) % HEIGHT) for r in robots]
        c40 = [r for r in at_end if r[0] == 40]
        avg_neigh = sum(len(pt.adj_ortho(r, c40)) for r in c40) / len(c40)
        if avg_neigh > 1.75:
            if output:
                img.print_image(at_end)
                print('t:', sec, 'avg neighbors in col 40:', avg_neigh)
            return sec
        sec += 1

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
