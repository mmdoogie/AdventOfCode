from mrm.iter import batched
from mrm.parse import all_nums

def parse():
    with open('data/aoc_2024/13.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return batched(lines, 4)

def parse_batch(g):
    a = tuple(all_nums(g[0]))
    b = tuple(all_nums(g[1]))
    p = tuple(all_nums(g[2]))

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
    batches = parse()
    score = 0
    for b in batches:
        a, b, p = parse_batch(b)
        m, n = solve(*a, *b, *p)
        if m > 100 or n > 100:
            continue
        score += 3*m + n
    return score

def part2(output=False):
    batches = parse()
    offset = 10000000000000
    score = 0
    for b in batches:
        a, b, p = parse_batch(b)
        p = (v + offset for v in p)
        m, n = solve(*a, *b, *p)
        score += 3*m + n
    return score

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
