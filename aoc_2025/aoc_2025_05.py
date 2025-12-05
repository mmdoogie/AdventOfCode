from mrm.util import merge_ranges

def parse():
    with open('data/aoc_2025/05.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    ranges = []
    ingrs = []
    for l in lines:
        if '-' in l:
            vals = [int(x) for x in l.split('-')]
            ranges += [range(vals[0], vals[1] + 1)]
            continue
        if l == '':
            continue
        ingrs += [int(l)]

    return ranges, ingrs

def part1(output=False):
    ranges, ingrs = parse()

    return sum(any(i in r for r in ranges) for i in ingrs)

def part2(output=False):
    ranges, _ = parse()

    ranges = merge_ranges(ranges)

    return sum(r.stop-r.start for r in ranges)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
