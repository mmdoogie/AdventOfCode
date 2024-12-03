import itertools

def parse():
    with open('data/aoc_2022/17.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

shapes = [["  @@@@ "], ["   @   ", "  @@@  ", "   @   "], ["  @@@  ", "    @  ", "    @  "], ["  @    ", "  @    ", "  @    ", "  @    "], ["  @@   ", "  @@   "]]

def part1(output=False):
    lines = parse()

    sh = itertools.cycle(shapes)
    j = itertools.cycle(iter(lines[0]))

    rows = ["-------"]
    for epoch in range(2022):
        rows += ["       ", "       ", "       "]
        rows += next(sh)
        
        if output and epoch % 100 == 0:
            print("Epoch", epoch)

        freeze = False
        while not freeze:
            push = next(j)
            leftEdge = [l.index("@") if "@" in l else -1 for l in rows]
            rightEdge = [l.rindex("@") if "@" in l else -1 for l in rows]

            if push == "<":
                if all([l == -1 or (l > 0 and rows[n][l-1] == " ") for n, l in enumerate(leftEdge)]):
                    for n, l in enumerate(rows):
                        if "@" not in l:
                            continue
                        rows[n] = l[0:leftEdge[n]-1] + l[leftEdge[n]:rightEdge[n]+1] + " " + l[rightEdge[n]+1:]
                        leftEdge[n] -= 1
                        rightEdge[n] -= 1
            if push == ">":
                if all([r == -1 or (r < 6 and rows[n][r+1] == " ") for n, r in enumerate(rightEdge)]):
                    for n, r in enumerate(rows):
                        if "@" not in r:
                            continue
                        rows[n] = r[0:leftEdge[n]] + " " + r[leftEdge[n]:rightEdge[n]+1] + r[rightEdge[n]+2:]
                        leftEdge[n] += 1
                        rightEdge[n] += 1

            freeze = False
            for y, r in enumerate(rows):
                if "@" not in r:
                    continue
                for x, c in enumerate(r):
                    if "@" not in c:
                        continue
                    if rows[y-1][x] not in "@ ":
                        freeze = True
                        break
                if freeze:
                    break

            for y, l in enumerate(rows):
                if "@" not in l:
                    continue

                if freeze:
                    rows[y] = rows[y].replace("@", "#")
                else:
                    rows[y-1] = rows[y-1][0:leftEdge[y]] + ("@"*(rightEdge[y]-leftEdge[y]+1)) + rows[y-1][rightEdge[y]+1:]
                    rows[y] = rows[y][0:leftEdge[y]] + (" "*(rightEdge[y]-leftEdge[y]+1)) + rows[y][rightEdge[y]+1:]

            if freeze:
                empties = [l == "       " for l in rows]
                lastRow = len(rows)
                for n, v in enumerate(reversed(empties)):
                    if v == False:
                        lastRow -= n
                        break
                        
                rows = rows[0:lastRow]

    return len(rows)-1

def part2(output=False):
    lines = parse()
    sh = itertools.cycle(shapes)
    j = itertools.cycle(iter(lines[0]))

    tops = [0]
    rows = ["-------"]
    for epoch in range(4000):
        rows += ["       ", "       ", "       "]
        rows += next(sh)

        if output and epoch % 100 == 0:
            print("Epoch", epoch)

        freeze = False
        while not freeze:
            push = next(j)
            
            leftEdge = [l.index("@") if "@" in l else -1 for l in rows]
            rightEdge = [l.rindex("@") if "@" in l else -1 for l in rows]

            if push == "<":
                if all([l == -1 or (l > 0 and rows[n][l-1] == " ") for n, l in enumerate(leftEdge)]):
                    for n, l in enumerate(rows):
                        if "@" not in l:
                            continue
                        rows[n] = l[0:leftEdge[n]-1] + l[leftEdge[n]:rightEdge[n]+1] + " " + l[rightEdge[n]+1:]
                        leftEdge[n] -= 1
                        rightEdge[n] -= 1
            if push == ">":
                if all([r == -1 or (r < 6 and rows[n][r+1] == " ") for n, r in enumerate(rightEdge)]):
                    for n, r in enumerate(rows):
                        if "@" not in r:
                            continue
                        rows[n] = r[0:leftEdge[n]] + " " + r[leftEdge[n]:rightEdge[n]+1] + r[rightEdge[n]+2:]
                        leftEdge[n] += 1
                        rightEdge[n] += 1

            freeze = False
            for y, r in enumerate(rows):
                if "@" not in r:
                    continue
                for x, c in enumerate(r):
                    if "@" not in c:
                        continue
                    if rows[y-1][x] not in "@ ":
                        freeze = True
                        break
                if freeze:
                    break

            for y, l in enumerate(rows):
                if "@" not in l:
                    continue

                if freeze:
                    rows[y] = rows[y].replace("@", "#")
                else:
                    rows[y-1] = rows[y-1][0:leftEdge[y]] + ("@"*(rightEdge[y]-leftEdge[y]+1)) + rows[y-1][rightEdge[y]+1:]
                    rows[y] = rows[y][0:leftEdge[y]] + (" "*(rightEdge[y]-leftEdge[y]+1)) + rows[y][rightEdge[y]+1:]

            if freeze:
                empties = [l == "       " for l in rows]
                lastRow = len(rows)
                for n, v in enumerate(reversed(empties)):
                    if v == False:
                        lastRow -= n
                        break
                        
                rows = rows[0:lastRow]
                tops += [lastRow-1]

    pat = rows[tops[250]:tops[250]+30]
    cyc = []
    for o in range(tops[250],len(rows)-30):
        if rows[o:o+30] == pat:
            if output:
                print("Cycle detected, offset", tops.index(o), tops[tops.index(o)])
            cyc += [(tops.index(o), tops[tops.index(o)])]

    if cyc[2][0] - cyc[1][0] == cyc[1][0] - cyc[0][0] and cyc[2][1] - cyc[1][1] == cyc[1][1] - cyc[0][1]:
        if output:
            print("Cycle confirmed")
        blocks = int(1e12)
        height = 0

        blocks -= 250
        height += tops[250]
        if output:
            print("Initial", 250, "blocks add", height)

        db = cyc[2][0] - cyc[1][0]
        dh = cyc[2][1] - cyc[1][1]

        cycles = blocks // db
        blocks -= (cycles) * db
        height += cycles * dh
        if output:
            print(cycles, "cycles add", dh, "now", height)

        dh = tops[250+blocks]-tops[250]
        if output:
            print(blocks, "remain add", dh)
        height += dh
        blocks -= blocks

        if output:
            print("final", height)
        return height
