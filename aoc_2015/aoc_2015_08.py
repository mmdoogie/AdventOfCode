import re

with open('data/aoc_2015/08.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

HEX = re.compile(r'\\x[0-9a-f]{2}')

def deescape_len(d):
    val = len(d) - 2
    esc_idx = [i for i, c in enumerate(d) if c == '\\']
    used = set()
    for e in esc_idx:
        if e in used:
            continue
        if d[e:e+2] in ['\\\\', '\\"']:
            val -= 1
            used.add(e)
            used.add(e + 1)
        elif HEX.match(d[e:e+4]):
            val -= 3
            used.add(e)
    return val

def reescape_len(d):
    return len(d) + 2 + sum(c in '"\\' for c in d)

def part1(output = True):
    size, deesc = 0, 0
    for d in dat:
        size += len(d)
        deesc += deescape_len(d)
    return size - deesc

def part2(output = True):
    size, reesc = 0, 0
    for d in dat:
        size += len(d)
        reesc += reescape_len(d)
    return reesc - size

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
