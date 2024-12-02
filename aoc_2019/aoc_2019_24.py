def parse():
    with open('data/aoc_2019/24.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    start_bugs = {}
    width, height = 0, 0
    for y, line in enumerate(dat):
        height = y + 1
        for x, c in enumerate(line):
            width = x + 1
            if c == '#':
                start_bugs[(x, y)] = True

    return height, width, start_bugs

def adj_bugs(loc, bugs):
    x, y = loc
    adj = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return sum([a in bugs for a in adj])

def biodiversity(height, width, bugs):
    total = 0
    for y in range(height):
        for x in range(width):
            if (x, y) in bugs:
                total += pow(2, (width * y + x))
    return total

def part1(output=False):
    height, width, bugs = parse()
    seen_bdr = {}

    while True:
        new_bugs = {}
        for y in range(height):
            for x in range(width):
                adj = adj_bugs((x, y), bugs)
                if (x, y) in bugs:
                    if adj == 1:
                        new_bugs[(x, y)] = True
                elif adj == 1 or adj == 2:
                    new_bugs[(x, y)] = True
        bdr = biodiversity(height, width, new_bugs)
        if bdr in seen_bdr:
            return bdr
        seen_bdr[bdr] = True
        bugs = new_bugs

def adj_recursive(loc, bugs):
    x, y, l = loc
    adj = set([(x-1, y, l), (x+1, y, l), (x, y-1, l), (x, y+1, l)])
    cnt = 0

    add_adj = set()
    rem_adj = set()
    for ax, ay, al in adj:
        if ax == 2 and ay == 2:
            rem_adj.add((ax, ay, al))
            if x == 1:
                add_adj.update([(0, iy, al+1) for iy in range(5)])
            elif x == 3:
                add_adj.update([(4, iy, al+1) for iy in range(5)])
            elif y == 1:
                add_adj.update([(ix, 0, al+1) for ix in range(5)])
            elif y == 3:
                add_adj.update([(ix, 4, al+1) for ix in range(5)])
        elif ax == -1:
            rem_adj.add((ax, ay, al))
            add_adj.add((1, 2, al-1))
        elif ax == 5:
            rem_adj.add((ax, ay, al))
            add_adj.add((3, 2, al-1))
        elif ay == -1:
            rem_adj.add((ax, ay, al))
            add_adj.add((2, 1, al-1))
        elif ay == 5:
            rem_adj.add((ax, ay, al))
            add_adj.add((2, 3, al-1))

    adj = adj.difference(rem_adj).union(add_adj)
    assert len(adj) == 4 or len(adj) == 8

    return sum([a in bugs for a in adj])

def part2(output=False):
    height, width, start_bugs = parse()
    bugs = {(x, y, 0): True for x, y in start_bugs}

    min_level = 0
    max_level = 0
    for t in range(200):
        new_bugs = {}
        for l in range(min_level-1, max_level+2):
            for y in range(height):
                for x in range(width):
                    if x == 2 and y == 2:
                        continue
                    adj = adj_recursive((x, y, l), bugs)
                    if (x, y, l) in bugs:
                        if adj == 1:
                            new_bugs[(x, y, l)] = True
                            if l < min_level:
                                min_level = l
                            if l > max_level:
                                max_level = l
                    elif adj == 1 or adj == 2:
                        new_bugs[(x, y, l)] = True
                        if l < min_level:
                            min_level = l
                        if l > max_level:
                            max_level = l
        bugs = new_bugs

    return len(bugs)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
