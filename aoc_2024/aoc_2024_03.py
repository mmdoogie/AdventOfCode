import re

def parse():
    with open('data/aoc_2024/03.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return ''.join(lines)

def do_mul(g1, g2):
    return int(g1) * int(g2)

def part1(output=False):
    lines = parse()
    mul_re = re.compile(r'mul\(([0-9]+),([0-9]+)\)')

    return sum(do_mul(*m.group(1, 2)) for m in mul_re.finditer(lines))

def part2(output=False):
    lines = parse()
    mul_re = re.compile(r"mul\(([0-9]+),([0-9]+)\)|do\(\)|don't\(\)")

    enabled = True
    total = 0
    for m in mul_re.finditer(lines):
        match m.group(0):
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                total += enabled * do_mul(*m.group(1, 2))

    return total

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
