from itertools import groupby
import re

def parse():
    with open('data/aoc_2024/13.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return groupby(lines, key=lambda l: l == '')

re_button = re.compile('Button [AB]: X[+]*([-0-9]+), Y[+]*([-0-9]+)')
re_prize = re.compile('Prize: X=([0-9]+), Y=([0-9]+)')

def parse_group(g):
    mat = re_button.match(next(g))
    a = (int(v) for v in mat.groups())
    mat = re_button.match(next(g))
    b = (int(v) for v in mat.groups())
    mat = re_prize.match(next(g))
    p = (int(v) for v in mat.groups())

    return a, b, p

def solve(ax, ay, bx, by, px, py):
    assert ax != 0 and ay !=0 and bx != 0 and by != 0

    m_num = by * px - bx * py
    m_denom = ax * by - ay * bx
    if m_num % m_denom != 0:
        return 0, 0

    n_num = ay * px - ax * py
    n_denom = ay * bx - ax * by
    if n_num % n_denom != 0:
        return 0, 0

    m = m_num // m_denom
    n = n_num // n_denom

    return m, n

def part1(output=False):
    groups = parse()
    score = 0
    for k, g in groups:
        if k:
            continue
        a, b, p = parse_group(g)
        m, n = solve(*a, *b, *p)
        if m > 100 or n > 100:
            continue
        score += 3*m + n
    return score

def part2(output=False):
    groups = parse()
    offset = 10000000000000
    score = 0
    for k, g in groups:
        if k:
            continue
        a, b, p = parse_group(g)
        p = (v + offset for v in p)
        m, n = solve(*a, *b, *p)
        score += 3*m + n
    return score

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
