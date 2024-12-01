def parse():
    with open('data/aoc_{YEAR}/{DAY}.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()
    return ''

def part2(output=False):
    lines = parse()
    return ''

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
