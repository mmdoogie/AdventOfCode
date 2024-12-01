from itertools import combinations

from mrm.util import product

with open('data/aoc_2015/02.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    paper_area = 0
    for box in dat:
        dims = list(sorted(int(x) for x in box.split('x')))
        for a, b in combinations(dims, 2):
            paper_area += 2 * a * b
        paper_area += dims[0] * dims[1]

    return paper_area

def part2(output = True):
    ribbon_len = 0
    for box in dat:
        dims = list(sorted(int(x) for x in box.split('x')))
        ribbon_len += 2 * (dims[0] + dims[1]) + product(dims)

    return ribbon_len

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
