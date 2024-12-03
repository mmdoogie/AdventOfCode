import functools

with open('data/aoc_2021/09.txt') as f:
    dat = [x.strip() for x in f.readlines()]

hmap = [[int(y) for y in list(x)] for x in dat]
xm = len(hmap[0])
ym = len(hmap)

def process_part1():
    score = 0
    minima = []

    for x in range(xm):
        for y in range(ym):
            h = hmap[y][x]
            l, r, u, d = 10, 10, 10, 10

            if x > 0:
                l = hmap[y][x-1]
            if x < xm - 1:
                r = hmap[y][x+1]
            if y > 0:
                u = hmap[y-1][x]
            if y < ym - 1:
                d = hmap[y+1][x]

            if all([h < v for v in [l, r, u, d]]):
                score += 1 + h
                minima += [(x, y)]

    return score, minima

def part1(output=False):
    score, _ = process_part1()
    return score

def exlocs(x, y):
    explore = set()
    
    if x > 0:
        explore.add((x-1, y))
    if x < xm - 1:
        explore.add((x+1, y))
    if y > 0:
        explore.add((x, y-1))
    if y < ym - 1:
        explore.add((x, y+1))
    
    return explore

def part2(output=False):
    _, minima = process_part1()
    basins = dict()
    for (x, y) in minima:
        explore = set()
        basin = 1

        explore.update(exlocs(x, y))
        hmap[y][x] = 10
        
        while len(explore) > 0:
            (ex, ey) = explore.pop()
            if hmap[ey][ex] < 9:
                basin += 1
                hmap[ey][ex] = 10
                explore.update(exlocs(ex, ey))
        basins[(x, y)] = basin

    result = functools.reduce(lambda a,b:a*b, sorted(basins.values(), reverse=True)[0:3])
    return result
