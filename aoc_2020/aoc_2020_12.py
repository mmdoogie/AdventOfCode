with open('data/aoc_2020/12.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output=False):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    turns = 0
    f_dir = dirs[turns % 4]
    loc = (0, 0)

    for d in dat:
        op = d[0]
        val = int(d[1:])

        if op == 'N':
            loc = (loc[0], loc[1] - val)
        elif op == 'E':
            loc = (loc[0] + val, loc[1])
        elif op == 'S':
            loc = (loc[0], loc[1] + val)
        elif op == 'W':
            loc = (loc[0] - val, loc[1])
        elif op == 'L':
            turns -= val // 90
            f_dir = dirs[turns % 4]
        elif op == 'R':
            turns += val // 90
            f_dir = dirs[turns % 4]
        elif op == 'F':
            loc = (loc[0] + val * f_dir[0], loc[1] + val * f_dir[1])

    return abs(loc[0]) + abs(loc[1])

def part2(output=False):
    loc = (0, 0)
    wpt = (10, -1)

    for d in dat:
        op = d[0]
        val = int(d[1:])

        if op == 'N':
            wpt = (wpt[0], wpt[1] - val)
        elif op == 'E':
            wpt = (wpt[0] + val, wpt[1])
        elif op == 'S':
            wpt = (wpt[0], wpt[1] + val)
        elif op == 'W':
            wpt = (wpt[0] - val, wpt[1])
        elif op == 'L':
            turns = val // 90
            for t in range(turns):
                wpt = (wpt[1], -wpt[0])
        elif op == 'R':
            turns = val // 90
            for t in range(turns):
                wpt = (-wpt[1], wpt[0])
        elif op == 'F':
            loc = (loc[0] + val * wpt[0], loc[1] + val * wpt[1])

    return abs(loc[0]) + abs(loc[1])
