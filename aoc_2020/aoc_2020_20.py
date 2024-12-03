import functools, operator, re

with open('data/aoc_2020/20.txt') as f:
    dat = [x.strip() for x in f.readlines()]

tiles = {}
currTileNum = 0
for d in dat:
    if ':' in d:
        currTileNum = int(d.split(' ')[1][:-1])
        tileDat = []
    elif d == '':
        tiles[currTileNum] = tileDat
    else:
        tileDat += [d]
tiles[currTileNum] = tileDat

def getBorders(tnum):
    top = tiles[tnum][0]
    bottom = tiles[tnum][9]
    left = ''.join([x[0] for x in tiles[tnum]])
    right = ''.join([x[9] for x in tiles[tnum]])

    tflip = top[::-1]
    bflip = bottom[::-1]
    lflip = left[::-1]
    rflip = right[::-1]

    return [top, bottom, left, right, tflip, bflip, lflip, rflip]

matches = {}
corners = []
for t in tiles.keys():
    mb = []
    borders = getBorders(t)[:4]
    for i, b in enumerate(borders):
        for tc in tiles.keys():
            if tc == t:
                continue
            candBorders = getBorders(tc)
            if b in candBorders:
                j = candBorders.index(b)
                mb += [(i, tc, j)]
    if len(mb) == 2:
        corners += [t]
    matches[t] = mb

cornerProd = functools.reduce(operator.mul, corners)

def getConf(t_bord, onto_bord):
    conf = {
        (0, 0): (True,  False,  2,  0, -1),
        (0, 1): (False, False,  0,  0,  1),
        (0, 2): (False, False,  1, -1,  0),
        (0, 3): (True,  False,  3,  1,  0),

        (0, 4): (False, False,  2,  0, -1),
        (0, 5): (True,  False,  0,  0,  1),
        (0, 6): (True,  False,  1, -1,  0),
        (0, 7): (False, False,  3,  1,  0),

        (1, 0): (False, False,  0,  0, -1),
        (1, 1): (True,  False,  2,  0,  1),
        (1, 2): (True,  False,  3, -1,  0),
        (1, 3): (False, False,  1,  1,  0),

        (1, 4): (True,  False,  0,  0, -1),
        (1, 5): (False, False,  2,  0,  1),
        (1, 6): (False, False,  3, -1,  0),
        (1, 7): (True,  False,  1,  1,  0),

        (2, 0): (False, False,  3,  0, -1),
        (2, 1): (False, True,   1,  0,  1),
        (2, 2): (False, True,   2, -1,  0),
        (2, 3): (False, False,  0,  1,  0),

        (2, 4): (False, True,   3,  0, -1),
        (2, 5): (False, False,  1,  0,  1),
        (2, 6): (False, False,  2, -1,  0),
        (2, 7): (False, True,   0,  1,  0),

        (3, 0): (False, True,   1,  0, -1),
        (3, 1): (False, False,  3,  0,  1),
        (3, 2): (False, False,  0, -1,  0),
        (3, 3): (False, True,   2,  1,  0),

        (3, 4): (False, False,  1,  0, -1),
        (3, 5): (False, True,   3,  0,  1),
        (3, 6): (False, True,   0, -1,  0),
        (3, 7): (False, False,  2,  1,  0),
    }

    return conf[(t_bord, onto_bord)]

def getPoints(tnum):
    p = set()
    for y in range(1, 9):
        for x in range(1, 9):
            if tiles[tnum][y][x] == '#':
                p.add((x-1, y-1))
    return p

def transform(pts, act):
    fliplr, flipud, rot, dx, dy = act
    rp = set()

    if rot == 2:
        fliplr = not fliplr
        flipud = not flipud
        rot = 0

    for p in pts:
        x, y = p

        if fliplr:
            ax = 7 - x
        else:
            ax = x

        if flipud:
            ay = 7 - y
        else:
            ay = y

        if rot == 3:
            ax, ay = ay, 7 - ax
        elif rot == 1:
            ax, ay = 7 - ay, ax

        rp.add((ax, ay))

    return rp

allPoints = getPoints(corners[0])
placed = {corners[0]: [(False, False, 0, 0, 0)]}
finpos = {corners[0]: (0, 0)}

def placeTile(tnum, t_bord, onto_bord, hist, onto_num):
    p = getPoints(tnum)
    conf = getConf(t_bord, onto_bord)


    for h in reversed(hist + [conf]):
        p = transform(p, h)

    cdx, cdy = finpos[onto_num]
    posact = [(1, 2)]
    for h in reversed(hist):
        posact = list(transform(posact, h))

    if conf[3] != 0:
        if posact[0][0] == 1:
            cdx += conf[3]
        elif posact[0][0] == 6:
            cdx -= conf[3]
        elif posact[0][1] == 6:
            cdy -= conf[3]
        elif posact[0][1] == 1:
            cdy += conf[3]
    elif conf[4] != 0:
        if posact[0][1] == 2:
            cdy += conf[4]
        elif posact[0][1] == 5:
            cdy -= conf[4]
        elif posact[0][0] == 5:
            cdx -= conf[4]
        elif posact[0][0] == 2:
            cdx += conf[4]

    for pt in p:
        dst = (pt[0] + 8*cdx, pt[1] + 8*cdy)
        allPoints.add(dst)

    placed[tnum] = hist + [conf]
    finpos[tnum] = (cdx, cdy)

def renderPoints():
    minX = min([p[0] for p in allPoints])
    minY = min([p[1] for p in allPoints])
    maxX = max([p[0] for p in allPoints])
    maxY = max([p[1] for p in allPoints])

    out = []
    for x in range(minX, maxX+1):
        line = []
        for y in range(minY, maxY+1):
            if (x, y) in allPoints:
                line += ['#']
            else:
                line += ['.']
        out += [''.join(line)]

    return out

while len(placed) < len(tiles):
    for p in placed.keys():
        added_one = False
        hist = placed[p]
        for mk, mv in matches.items():
            if mk not in placed:
                for (i, tc, j) in mv:
                    if p == tc:
                        placeTile(mk, i, j, hist, p)
                        added_one = True
        if added_one:
            break

outp = renderPoints()
ml1 = re.compile("[.#]{18}#")
ml2 = re.compile("#[.#]{4}##[.#]{4}##[.#]{4}###")
ml3 = re.compile("[.#]#[.#]{2}#[.#]{2}#[.#]{2}#[.#]{2}#[.#]{2}#")

seamonsters = 0
for i, l in enumerate(outp):
    start = 0
    while True:
        cand = ml2.search(l, start)
        if cand:
            prl = ml1.match(outp[i-1], cand.start())
            nxl = ml3.match(outp[i+1], cand.start())
            if prl and nxl:
                seamonsters += 1
            start = cand.start() + 1
        else:
            break

def part1(output=False):
    return cornerProd

def part2(output=False):
    return len(allPoints) - 15*seamonsters
