import math

def parse():
    with open('data/aoc_2025/02.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    rngs = []
    for l in lines[0].split(','):
        a, b = l.split('-')
        if len(a) == len(b):
            rngs += [range(int(a), int(b) + 1)]
        else:
            rngs += [range(int(a), int('9' * len(a)) + 1)]
            rngs += [range(int('9' * len(a)) + 1, int(b) + 1)]
    return rngs

def part1(output=False):
    rngs = parse()

    tot = 0
    for r in rngs:
        len_min = len(str(min(r)))

        if len_min % 2 == 1:
            continue

        pfx_min = str(min(r))[:len_min//2]
        pfx_max = str(max(r))[:len_min//2]

        for pfx in range(int(pfx_min), int(pfx_max) + 1):
            chk = int(str(pfx) * 2)
            if chk not in r:
                continue
            tot += chk

    return tot

def part2(output=False):
    rngs = parse()

    invalid = set()
    for r in rngs:
        len_min = len(str(min(r)))

        for pfx_len in range(1, math.ceil(len_min / 2) + 1):
            if len_min % pfx_len != 0:
                continue
            pfx_reps = len_min // pfx_len
            if pfx_reps < 2:
                continue

            pfx_min = str(min(r))[:pfx_len]
            pfx_max = str(max(r))[:pfx_len]

            for pfx in range(int(pfx_min), int(pfx_max) + 1):
                chk = int(str(pfx) * pfx_reps)
                if chk not in r:
                    continue
                invalid.add(chk)

    return sum(invalid)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
