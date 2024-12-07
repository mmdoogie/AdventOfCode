from itertools import product
from math import ceil, log10
import operator

def parse():
    with open('data/aoc_2024/07.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    equations = {}
    for l in lines:
        result, nums = l.split(': ')
        result = int(result)
        nums = [int(n) for n in nums.split(' ')]
        equations[result] = nums
    return equations

def print_eqn(result, nums, ops):
    print(result, '=', nums[0], end='')
    val = nums[0]
    for op, n in zip(ops, nums[1:]):
        if op is operator.add:
            print(f' + {n}', end='')
            val += n
        if op is operator.mul:
            print(f' * {n}', end='')
            val *= n
        if op is op_concat:
            print(f' = {val} || {n} -> {val}{n}', end='')
            val = op_concat(val, n)
    print()

def has_valid_ops(op_set, result, nums, output):
    pfx_len = 0
    pfx = []
    for ops in product(op_set, repeat=len(nums) - 1):
        if ops[:pfx_len] == pfx:
            continue
        val = nums[0]
        pfx_len = 0
        for op, n in zip(ops, nums[1:]):
            val = op(val, n)
            pfx_len += 1
            if val > result:
                break
        if val == result:
            if output:
                print_eqn(result, nums, ops)
            return True
        pfx = ops[:pfx_len]
    return False

def part1(output=False):
    equations = parse()
    op_set = {operator.mul, operator.add}
    return sum(result * has_valid_ops(op_set, result, nums, output) for result, nums in equations.items())

def op_concat(num_a, num_b):
    return num_a * 10**ceil(log10(num_b + 0.1)) + num_b

def part2(output=False):
    equations = parse()
    op_set = {op_concat, operator.mul, operator.add}
    return sum(result * has_valid_ops(op_set, result, nums, output) for result, nums in equations.items())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
