with open('data/aoc_2021/11.txt') as f:
    dat = [x.strip() for x in f.readlines()]
omap = [[int(y) for y in list(x)] for x in dat]
sx = len(omap[0])
sy = len(omap)

def plusup(omap):
    return [[y+1 for y in x] for x in omap]

def neighbors(x, y):
    n = list()
    if x > 0:
        n += [(x-1, y)]

    if x < sx - 1:
        n += [(x+1, y)]

    if y > 0:
        n += [(x, y-1)]
    
    if y < sy - 1:
        n += [(x, y+1)]
        
    if x > 0 and y > 0:
        n += [(x-1, y-1)]
    
    if x > 0 and y < sy - 1:
        n += [(x-1, y+1)]
    
    if x < sx - 1 and y > 0:
        n += [(x+1, y-1)]
    
    if x < sx - 1 and y < sx - 1:
        n += [(x+1, y+1)]
    
    return n

def flash(omap, x, y, excl):
    n = neighbors(x, y)
    for (nx, ny) in n:
        omap[ny][nx] += 1
        if omap[ny][nx] > 9 and (nx, ny) not in excl:
            excl.add((nx, ny))
            flash(omap, nx, ny, excl)

def part1(output=False):
    omap = [[int(y) for y in list(x)] for x in dat]
    flashCount = 0
    for i in range(100):
        omap = plusup(omap)
        flashed = set()

        for y in range(sy):
            for x in range(sx):
                if omap[y][x] > 9 and (x, y) not in flashed:
                    flashed.add((x,y))
                    flash(omap, x, y, flashed)

        flashCount += len(flashed)
        for (x, y) in flashed:
            omap[y][x] = 0

    return flashCount

def part2(output=False):
    omap = [[int(y) for y in list(x)] for x in dat]

    flashCount = 0
    it = 0
    while flashCount != 100:
        omap = plusup(omap)
        flashed = set()

        for y in range(sy):
            for x in range(sx):
                if omap[y][x] > 9 and (x, y) not in flashed:
                    flashed.add((x,y))
                    flash(omap, x, y, flashed)

        flashCount = len(flashed)
        for (x, y) in flashed:
            omap[y][x] = 0
        it += 1

    return it
