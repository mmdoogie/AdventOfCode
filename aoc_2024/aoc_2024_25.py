from itertools import groupby, product

from mrm.ansi_term import red, green, yellow

def parse():
    with open('data/aoc_2024/25.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    keys = []
    locks = []
    for is_pat, pat in groupby(lines, key=lambda x: x != ''):
        if not is_pat:
            continue
        pat = list(pat)
        curr = tuple(sum(p[i] == '#' for p in pat) for i in range(len(pat[0])))
        if '#' in pat[0]:
            locks += [curr]
        else:
            keys += [curr]

    return locks, keys

def part1(output=False):
    locks, keys = parse()
    match = sum(all(lx + kx <= 7 for lx, kx in zip(l, k)) for l, k in product(locks, keys))

    if output:
        for l, k in product(locks, keys):
            print('Lock', l, 'vs Key', k)
            conflict = False
            for r in range(7):
                row = []
                for lx, kx in zip(l, k):
                    if 7 - kx <= r < lx:
                        row += [red('X')]
                        conflict = True
                    elif r < lx:
                        row += [yellow('$')]
                    elif 7 - kx <= r:
                        row += [green('^')]
                    else:
                        row += ['.']
                print(''.join(row))
            if conflict:
                print(red('Key Overlaps!'))
            else:
                print(green('Key Fits!'))
            print()

    return match

def part2(output=False):
    return 'Deliver!'

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
