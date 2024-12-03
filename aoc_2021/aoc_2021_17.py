import re

with open('data/aoc_2021/17.txt') as f:
    dat = [x.strip() for x in f.readlines()]
r = re.compile('.*x=([-0-9]*)\.\.([-0-9]*), y=([-0-9]*)\.\.([-0-9]*)')
g = r.match(dat[0]).groups()
targetX = [int(x) for x in g[0:2]]
targetY = [int(x) for x in g[2:4]]

def hit(xvel, yvel):
    maxY = 0
    x = 0
    y = 0
    while True:
        x += xvel
        y += yvel
        maxY = max(y, maxY)
        if x >= targetX[0] and x <= targetX[1] and y >= targetY[0] and y <= targetY[1]:
            return maxY
        if x > targetX[1] or y < targetY[0]:
            return None
        if xvel > 0:
            xvel -= 1
        elif xvel < 0:
            xvel += 1
        yvel -= 1

def compute():
    maxH = 0
    maxHv = (0, 0)
    cntH = 0
    for yv in range(-110, 500):
        for xv in range(0, 260):
            h = hit(xv, yv)
            if h is None:
                continue
            cntH += 1
            if h > maxH:
                maxH = h
                maxHv = (xv, yv)

    return maxH, cntH

def part1(output=False):
    maxH, _ = compute()
    return maxH

def part2(output=False):
    _, cntH = compute()
    return cntH
