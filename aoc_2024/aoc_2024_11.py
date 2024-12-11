from collections import defaultdict

def parse():
    with open('data/aoc_2024/11.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    vals = [int(x) for x in lines[0].split(' ')]
    return defaultdict(int, {v: sum(val == v for val in vals) for v in vals})

def blink(rocks):
    updates = defaultdict(int)
    for rk, rv in rocks.items():
        if rk == 0:
            updates[0] -= rv
            updates[1] += rv
            continue
        rk_str = str(rk)
        rk_len = len(rk_str)
        if rk_len % 2 == 0:
            left_half  = int(rk_str[:rk_len // 2])
            right_half = int(rk_str[rk_len // 2:])
            updates[rk] -= rv
            updates[left_half] += rv
            updates[right_half] += rv
            continue
        updates[rk] -= rv
        updates[rk * 2024] += rv
    for uk, uv in updates.items():
        rocks[uk] += uv

def part1(output=False):
    rocks = parse()
    for _ in range(25):
        blink(rocks)
    return sum(rocks.values())

def part2(output=False):
    rocks = parse()
    for _ in range(75):
        blink(rocks)
    return sum(rocks.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
