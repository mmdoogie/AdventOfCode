def parse():
    with open('data/aoc_2024/05.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def passing(rules, p):
    ok = True
    for r in rules:
        if r[0] in p and r[1] in p:
            if p.index(r[0]) > p.index(r[1]):
                ok = False
                break
    return ok

def part1(output=False):
    lines = parse()
    rules = [tuple(int(x) for x in l.split('|')) for l in lines if '|' in l]
    pages = [tuple(int(x) for x in l.split(',')) for l in lines if ',' in l]

    ok = [p for p in pages if passing(rules, p)]
    return sum(p[len(p) // 2] for p in ok)

def fixup(rules, p):
    p = list(p)
    rules = [r for r in rules if r[0] in p and r[1] in p]
    while not passing(rules, p):
        for r in rules:
            i0 = p.index(r[0])
            i1 = p.index(r[1])
            if i0 < i1:
                continue
            p[i0], p[i1] = p[i1], p[i0]
    return p

def part2(output=False):
    lines = parse()
    rules = [tuple(int(x) for x in l.split('|')) for l in lines if '|' in l]
    pages = [tuple(int(x) for x in l.split(',')) for l in lines if ',' in l]

    fixed = [fixup(rules, p) for p in pages if not passing(rules, p)]
    return sum(p[len(p) // 2] for p in fixed)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
