from collections import deque

with open('data/aoc_2020/15.txt') as f:
    dat = [x.strip() for x in f.readlines()]

inp = [int(x) for x in dat[0].split(',')]

def part1(output=False):
    nums = inp[:]

    turn = len(nums)
    while turn < 2020:
        prev = nums[-1]

        if prev not in nums[:-1]:
            last_occ = 0
        else:
            last_occ = list(reversed(nums[:-1])).index(prev) + 1

        nums += [last_occ]
        turn += 1

    return nums[-1]

def part2(output=False):
    lastTurn = {}
    for i, n in enumerate(inp[:-1]):
        lastTurn[n] = i

    turn = len(inp)
    prev = inp[-1]

    while turn < 30000000:
        if prev not in lastTurn:
            last_occ = 0
        else:
            last_occ = turn - lastTurn[prev] - 1

        lastTurn[prev] = turn - 1
        prev = last_occ
        turn += 1

    return last_occ
