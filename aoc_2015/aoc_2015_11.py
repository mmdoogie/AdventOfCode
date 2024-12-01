from collections import Counter
import re
from string import ascii_lowercase

from mrm.text import let2num, num2let
from mrm.iter import sliding_window

with open('data/aoc_2015/11.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def pwd_incr(seed):
    vals = [let2num(x) for x in seed]
    while True:
        vals[-1] += 1
        vals = [v % 26 + (vals[i + 1] if i != len(vals) - 1 else 0) // 26 for i, v in enumerate(vals)]
        yield ''.join([num2let(x) for x in vals])

pairs = re.compile(r'([a-z])\1')

def pwd_is_valid(pwd):
    if any(c in pwd for c in 'iol'):
        return False
    pc = Counter(pairs.findall(pwd))
    if sum(v > 0 for v in pc.values()) < 2:
        return False
    if any(''.join(t) in pwd for t in sliding_window(ascii_lowercase, 3)):
        return True
    return False

def valid_pwd_gen(seed):
    g = pwd_incr(dat[0])
    while True:
        pwd = next(g)
        if pwd_is_valid(pwd):
            yield pwd

def part1(output = True):
    v = valid_pwd_gen(dat[0])
    return next(v)

def part2(output = True):
    v = valid_pwd_gen(dat[0])
    _ = next(v)
    return next(v)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
