from collections import deque

with open('data/aoc_2020/23.txt') as f:
    dat = [x.strip() for x in f.readlines()]

cups = [int(c) for c in dat[0]]

def part1(output=False):
    c = deque(cups)

    minlbl, maxlbl = min(c), max(c)

    dist = 0
    c.rotate(-4)
    for m in range(100):
        rem = [c.pop(), c.pop(), c.pop()]
        dstlbl = c[-1] - 1
        if dstlbl < minlbl:
            dstlbl = maxlbl
        while dstlbl in rem:
            dstlbl -= 1
            if dstlbl < minlbl:
                dstlbl = maxlbl
        dist = c.index(dstlbl) + 1
        c.rotate(-dist)
        c.extend(reversed(rem))
        c.rotate(dist-1)

    c.rotate(-c.index(1))
    return ''.join(str(x) for x in list(c)[1:])

def part2(output=False):
    nextCups = {}
    prev = None
    for c in cups:
        if prev:
            nextCups[prev] = c
        prev = c
    for c in range(max(cups)+1, 1000000+1):
        nextCups[prev] = c
        prev = c
    nextCups[prev] = cups[0]

    mincup = min(nextCups.keys())
    maxcup = max(nextCups.keys())

    cidx = cups[0]
    for m in range(10000000):
        r1 = nextCups[cidx]
        r2 = nextCups[r1]
        r3 = nextCups[r2]
        nextCups[cidx] = nextCups[r3]
        dst = cidx - 1
        if dst < mincup:
            dst = maxcup
        while dst in [r1, r2, r3]:
            dst -= 1
            if dst < mincup:
                dst = maxcup
        nn = nextCups[dst]
        nextCups[dst] = r1
        nextCups[r1] = r2
        nextCups[r2] = r3
        nextCups[r3] = nn
        cidx = nextCups[cidx]
        if cidx > maxcup:
            cidx = mincup
    
    return nextCups[1] * nextCups[nextCups[1]]
