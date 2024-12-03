import math
def parse():
    with open('data/aoc_2022/24.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def compute(output):
    lines = parse()
    width = len(lines[0])
    height = len(lines)

    blizzards = []
    dirFromSym = {">": (1, 0), "v": (0, 1), "^": (0, -1), "<": (-1, 0)}

    for y, l in enumerate(lines):
        for x, c in enumerate(list(l)):
            if c in ">v^<":
                blizzards += [[x, y, c]]

    gStartPos = (1, 0)
    gEndPos = (lines[-1].index("."), height - 1)

    et = []

    paths = {gStartPos}
    endPos = gEndPos
    t = 1
    bestProg = 100000
    bpp = gStartPos
    while len(et) != 3:
        if output and t == 1:
            print("Phase", len(et) + 1)

        for b in blizzards:
            bd = dirFromSym[b[2]]
            b[0] += bd[0]
            b[1] += bd[1]

            if bd[0] == -1 and b[0] == 0:
                b[0] = width - 2
            if bd[0] == 1 and b[0] == width - 1:
                b[0] = 1
            if bd[1] == -1 and b[1] == 0:
                b[1] = height - 2
            if bd[1] == 1 and b[1] == height - 1:
                b[1] = 1

        blizzPos = set([(b[0], b[1]) for b in blizzards])

        newPaths = set()
        for p in paths:
            prog = abs(p[0] - endPos[0]) + abs(p[1] - endPos[1])
            
            if p not in blizzPos:
                newPaths.add(p)
            
            for c, bd in dirFromSym.items():
                pp = (p[0] + bd[0], p[1] + bd[1])
                if pp == endPos:
                    et += [t]
                    t = 0
                    bestProg = 100000
                    if len(et) == 1:
                        bpp = gEndPos
                        newPaths = {gEndPos}
                        endPos = gStartPos
                    else:
                        bpp = gStartPos
                        newPaths = {gStartPos}
                        endPos = gEndPos
                    break
                if pp[0] <= 0 or pp[0] >= width - 1 or pp[1] <= 0 or pp[1] >= height - 1:
                    continue
                if pp not in blizzPos:
                    newPaths.add(pp)
                    
                    prog = abs(pp[0] - endPos[0]) + abs(pp[1] - endPos[1])
                    if prog < bestProg:
                        bestProg = prog
                        bpp = pp
                        if output:
                            print(t, pp, bestProg)
            if t == 0:
                break
        paths = newPaths
        t += 1
    return et

def part1(output=False):
    et = compute(output)
    return et[0]

def part2(output=False):
    et = compute(output)
    return sum(et)
