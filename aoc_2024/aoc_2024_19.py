from functools import cache

def parse():
    with open('data/aoc_2024/19.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    towels = set(lines[0].split(', '))
    patterns = lines[2:]

    return towels, patterns

def part1(output=False):
    towels, patterns = parse()

    @cache
    def valid_pattern(p):
        if p == '':
            return True
        for t in towels:
            if p.startswith(t) and valid_pattern(p[len(t):]):
                return True
        return False

    return sum(valid_pattern(p) for p in patterns)

def part2(output=False):
    towels, patterns = parse()

    @cache
    def num_patterns(p):
        if p == '':
            return 1
        return sum(num_patterns(p[len(t):]) for t in towels if p.startswith(t))

    return sum(num_patterns(p) for p in patterns)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
