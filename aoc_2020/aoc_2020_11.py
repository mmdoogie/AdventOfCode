with open('data/aoc_2020/11.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def neighcnt(loc, occ):
    x, y = loc
    cnt = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx != 0 or dy != 0:
                chk = (x + dx, y + dy)
                if chk in occ:
                    cnt += 1
    return cnt

def part1(output=False):
    s_empty = set()
    s_occ = set()

    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            if c == 'L':
                s_empty.add((x, y))
            elif c == '#':
                s_occ.add((x, y))

    while True:
        new_empty = set()
        new_occ = set()
        changed = False

        for s in s_empty:
            if neighcnt(s, s_occ) == 0:
                changed = True
                new_occ.add(s)
            else:
                new_empty.add(s)

        for s in s_occ:
            if neighcnt(s, s_occ) >= 4:
                changed = True
                new_empty.add(s)
            else:
                new_occ.add(s)

        s_empty = new_empty
        s_occ = new_occ

        if not changed:
            return len(new_occ)

def visneigh(loc, occ, emp, maxX, maxY):
    x, y = loc
    cnt = 0

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in dirs:
        i = 1
        while True:
            cx = x + i * dx
            cy = y + i * dy
            if cx < 0 or cx > maxX or cy < 0 or cy > maxY:
                break
            if (cx, cy) in emp:
                break
            if (cx, cy) in occ:
                cnt += 1
                break
            i += 1

    return cnt

def part2(output=False):
    s_empty = set()
    s_occ = set()

    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            if c == 'L':
                s_empty.add((x, y))
            elif c == '#':
                s_occ.add((x, y))

    maxX = max([s[0] for s in s_occ.union(s_empty)])
    maxY = max([s[1] for s in s_occ.union(s_empty)])

    while True:
        new_empty = set()
        new_occ = set()
        changed = False

        for s in s_empty:
            if visneigh(s, s_occ, s_empty, maxX, maxY) == 0:
                changed = True
                new_occ.add(s)
            else:
                new_empty.add(s)

        for s in s_occ:
            if visneigh(s, s_occ, s_empty, maxX, maxY) >= 5:
                changed = True
                new_empty.add(s)
            else:
                new_occ.add(s)

        s_empty = new_empty
        s_occ = new_occ

        if not changed:
            return len(new_occ)
