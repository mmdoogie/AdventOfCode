from itertools import pairwise

def parse():
    with open('data/aoc_2024/02.txt', 'r', encoding='utf8') as f:
        reports = [[int(x) for x in l.strip('\n').split()] for l in f.readlines()]
    return reports

def safe(report):
    delta = [a - b for a, b in pairwise(report)]
    ordered = all(d > 0 for d in delta) or all(d < 0 for d in delta)
    constrained = all(1 <= abs(d) <= 3 for d in delta)
    return ordered and constrained

def one_outs(report):
    return (report[:i] + report[i+1:] for i in range(len(report)))

def part1(output=False):
    reports = parse()
    return sum(safe(r) for r in reports)

def part2(output=False):
    reports = parse()
    return sum(safe(r) or any(safe(o) for o in one_outs(r)) for r in reports)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
