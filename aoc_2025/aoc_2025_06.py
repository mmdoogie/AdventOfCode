import string

from mrm.parse import all_nums
from mrm.util import big_pi

def parse():
    with open('data/aoc_2025/06.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()

    vals = [list(all_nums(l)) for l in lines[:-1]]
    ops = [{'*': big_pi, '+': sum}[c] for c in lines[-1] if c in '*+']

    tot = sum(prob_op(prob_vals) for prob_op, *prob_vals in zip(ops, *vals))

    return tot

def part2(output=False):
    lines = parse()

    tot = 0
    nums = []
    for i in range(len(lines[0]) - 1, -1, -1):
        num_str = ''.join([l[i] for l in lines[:-1] if l[i] in string.digits])
        if not num_str:
            continue
        num_val = int(num_str)
        nums += [num_val]
        if lines[-1][i] == '*':
            tot += big_pi(nums)
            nums = []
        if lines[-1][i] == '+':
            tot += sum(nums)
            nums = []

    return tot

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
