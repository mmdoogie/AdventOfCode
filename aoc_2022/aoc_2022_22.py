import re

def parse():
    with open('data/aoc_2022/22.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = lines[0:-2]
    instr = lines[-1]

    rx = re.compile("([0-9]+)([LR])?")
    steps = rx.findall(instr)

    return grid, steps

def part1(output=False):
    grid, steps = parse()

    gwidth = max([len(g) for g in grid])
    grid = [str.ljust(g, gwidth, " ") for g in grid]

    gleft = []
    gright = []
    gtop = [1000]*gwidth
    gbot = [0]*gwidth
    for y,g in enumerate(grid):
        if "#" not in g:
            gleft += [g.index(".")]
            gright += [g.rindex(".")]
        else:
            gleft += [min(g.index("."), g.index("#"))]
            gright += [max(g.rindex("."), g.rindex("#"))]
        for n in range(gleft[y],gright[y]+1):
            if y < gtop[n]:
                gtop[n] = y
            if y > gbot[n]:
                gbot[n] = y

    pos = [gleft[0], 0]
    hdgs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    face = [">", "v", "<", "^"]
    hidx = 0

    for s in steps:
        for n in range(int(s[0])):
            np = [pos[0] + hdgs[hidx][0], pos[1] + hdgs[hidx][1]]
            if hdgs[hidx][0] != 0:
                if np[0] > gright[np[1]]:
                    np[0] = gleft[np[1]]
                if np[0] < gleft[np[1]]:
                    np[0] = gright[np[1]]
            else:
                if np[1] > gbot[np[0]]:
                    np[1] = gtop[np[0]]
                if np[1] < gtop[np[0]]:
                    np[1] = gbot[np[0]]
            npc = grid[np[1]][np[0]]
            assert npc != " "
            if npc == "#":
                break
            pos = np
            assert grid[pos[1]][pos[0]] != "#"
            gs = [*grid[pos[1]]]
            gs[pos[0]] = face[hidx]
            grid[pos[1]] = ''.join(gs)
        if s[1] == "R":
            hidx += 1
            if hidx > 3:
                hidx = 0
        elif s[1] == "L":
            hidx -= 1
            if hidx < 0:
                hidx = 3

    if output:
        print("Final Pos:", pos, "Heading:", hidx, face[hidx])
        print("Code:", 1000*(pos[1]+1) + 4*(pos[0]+1) + hidx)
    
    return 1000*(pos[1]+1) + 4*(pos[0]+1) + hidx

def part2(output=False):
    grid, steps = parse()

    gwidth = max([len(g) for g in grid])
    grid = [str.ljust(g, gwidth, " ") for g in grid]
    gheight = len(grid)

    gleft = []
    gright = []
    gtop = [1000]*gwidth
    gbot = [0]*gwidth
    for y,g in enumerate(grid):
        if "#" not in g:
            gleft += [g.index(".")]
            gright += [g.rindex(".")]
        else:
            gleft += [min(g.index("."), g.index("#"))]
            gright += [max(g.rindex("."), g.rindex("#"))]
        for n in range(gleft[y],gright[y]+1):
            if y < gtop[n]:
                gtop[n] = y
            if y > gbot[n]:
                gbot[n] = y

    pos = [gleft[0], 0]
    hdgs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    face = [">", "v", "<", "^"]
    hidx = 0

    def getSide(pos):
        if pos[1] < 50:
            if pos[0] >= 50 and pos[0] < 100:
                return 1
            elif pos[0] >= 100 and pos[0] < 150:
                return 2
        elif pos[1] < 100:
            if pos[0] >= 50 and pos[0] < 100:
                return 3
        elif pos[1] < 150:
            if pos[0] < 50:
                return 4
            elif pos[0] < 100:
                return 5
        elif pos[1] < 200 and pos[0] < 50:
            return 6

    def teleport(pos, hidx):
        ss = getSide(pos)
        if ss == 1:
            if hidx == 3:
                os = pos[0] - 50
                return ([0, 150 + os], 0)
            elif hidx == 2:
                os = pos[1]
                return ([0, 149 - os], 0)
        elif ss == 2:
            if hidx == 3:
                os = pos[0] - 100
                return ([os, 199], 3)
            elif hidx == 1:
                os = pos[0] - 100
                return ([99, 50 + os], 2)
            elif hidx == 0:
                os = pos[1]
                return ([99, 149 - os], 2)
        elif ss == 3:
            if hidx == 2:
                os = pos[1] - 50
                return ([os, 100], 1)
            elif hidx == 0:
                os = pos[1] - 50
                return ([100 + os, 49], 3)
        elif ss == 4:
            if hidx == 3:
                os = pos[0]
                return ([50, 50 + os], 0)
            elif hidx == 2:
                os = pos[1] - 100
                return ([50, 49 - os], 0)
        elif ss == 5:
            if hidx == 0:
                os = pos[1] - 100
                return ([149, 49 - os], 2)
            elif hidx == 1:
                os = pos[0] - 50
                return ([49, 150 + os], 2)
        elif ss == 6:
            if hidx == 1:
                os = pos[0]
                return ([100 + os, 0], 1)
            elif hidx == 2:
                os = pos[1] - 150
                return ([50 + os, 0], 1)
            elif hidx == 0:
                os = pos[1] - 150
                return ([os + 50, 149], 3)

    for s in steps:
        for n in range(int(s[0])):
            if any([pos[0] == gleft[pos[1]] and hidx == 2, pos[0] == gright[pos[1]] and hidx == 0,
                    pos[1] == gtop[pos[0]] and hidx == 3, pos[1] == gbot[pos[0]] and hidx == 1]):
                (np, nd) = teleport(pos, hidx)
            else:
                np = [pos[0] + hdgs[hidx][0], pos[1] + hdgs[hidx][1]]
                nd = hidx
            npc = grid[np[1]][np[0]]
            assert npc != " "
            if npc == "#":
                break
            pos, hidx = np, nd
            gs = [*grid[pos[1]]]
            gs[pos[0]] = face[hidx]
            grid[pos[1]] = ''.join(gs)
        if s[1] == "R":
            hidx += 1
            if hidx > 3:
                hidx = 0
        elif s[1] == "L":
            hidx -= 1
            if hidx < 0:
                hidx = 3

    if output:
        print("Final Pos:", pos, "Heading:", hidx, face[hidx])
        print("Code:", 1000*(pos[1]+1) + 4*(pos[0]+1) + hidx)
    
    return 1000*(pos[1]+1) + 4*(pos[0]+1) + hidx
