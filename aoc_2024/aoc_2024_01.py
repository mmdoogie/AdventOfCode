def parse():
    with open('data/aoc_2024/01.txt', encoding = 'utf-8') as f:
        dat = [x.strip('\n') for x in f.readlines()]
    values = [[int(x) for x in d.split()] for d in dat]
    left = [v[0] for v in values]
    right = [v[1] for v in values]
    return left, right

def part1(output = True):
    left, right = parse()
    tot = sum(abs(a - b) for a, b in zip(sorted(left), sorted(right)))
    return tot

def part2(output = True):
    left, right = parse()
    tot = sum(l * sum(r == l for r in right) for l in left)
    return tot

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
