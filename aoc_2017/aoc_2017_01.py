from itertools import pairwise

with open('data/aoc_2017/01.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    nums = [int(x) for x in dat[0]]

def part1(output = True):
    del output

    val = sum(x for x, y in pairwise(nums + [nums[0]]) if x == y)

    return val

def part2(output = True):
    del output

    split = len(nums) // 2
    val = 2 * sum(x for x, y in zip(nums[:split], nums[split:]) if x == y)

    return val

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
