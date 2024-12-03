import math
def parse():
    with open('data/aoc_2022/25.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

symToDigits = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
digitsToSym = {v: k for k, v in symToDigits.items()}

def fromBaseWeird(s):
    global symToDigits
    n = 0
    x = 0
    for d in reversed(list(s)):
        n += symToDigits[d] * 5 ** x
        x += 1
    return n

def toBaseWeird(n):
    x = math.floor(math.log(n, 5))
    s = [0] * (x + 1)
    for o in range(x, -1, -1):
        exa = 5 ** o
        d = int(round(n / exa, 0))
        n -= d * exa
        s[o] = d
        o -= 1
    return ''.join([digitsToSym[d] for d in reversed(s)])

def part1(output=False):
    lines = parse()
    total = sum(fromBaseWeird(l) for l in lines)
    return toBaseWeird(total)

def part2(output=False):
    return 'Start!'
