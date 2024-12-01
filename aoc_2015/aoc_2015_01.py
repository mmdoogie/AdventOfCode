with open('data/aoc_2015/01.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    floor = 0
    for c in dat[0]:
        if c == '(':
            floor += 1
        if c == ')':
            floor -= 1
    return floor

def part2(output = True):
    floor = 0
    for i, c in enumerate(dat[0]):
        if c == '(':
            floor += 1
        if c == ')':
            floor -= 1
        if floor == -1:
            return i + 1
    return 0

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
