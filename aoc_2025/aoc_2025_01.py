from itertools import accumulate

def parse():
    with open('data/aoc_2025/01.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [(-1 if l[0] == 'L' else 1) * int(l[1:]) for l in lines]

def part1(output=False):
    turns = parse()

    positions = accumulate(turns, lambda a, b: (a + b) % 100, initial=50)

    if output:
        password = 0
        for (t, p) in zip(turns, positions):
            if not p:
                password += 1
            print(f'After turn {t:4} position is {p:2}{"*" if not p else " "} {password}')
    else:
        password = sum(1 for p in positions if not p)

    return password

def part2(output=False):
    turns = parse()

    knob_at = 50
    password = 0
    for t in turns:
        if output:
            print(f'After turn {t:4}', end=' ')
        crosses = 0
        if t < 0:
            if knob_at and knob_at + t <= 0:
                t += knob_at
                crosses += 1
                knob_at = 0
            crosses += -t // 100
        else:
            if knob_at and knob_at + t >= 100:
                t += knob_at - 100
                crosses += 1
                knob_at = 0
            crosses += t // 100
        knob_at = (knob_at + t) % 100
        password += crosses
        if output:
            print(f'position is {knob_at:2} {"*" if crosses else " "} (+{crosses:2}) {password}')

    return password

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
