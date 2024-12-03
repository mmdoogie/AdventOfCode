with open('data/aoc_2021/25.txt', 'r') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output=False):
    w = len(dat[0])
    h = len(dat)

    eastCukes = set()
    southCukes = set()
    for y, r in enumerate(dat):
        for x, c in enumerate(r):
            if c == '>':
                eastCukes.add((x, y))
            elif c == 'v':
                southCukes.add((x, y))

    i = 0
    while True:
        eastMoves = set()
        eastDests = set()
        for e in eastCukes:
            dest = ((e[0] + 1) % w, e[1])
            if dest not in eastCukes and dest not in southCukes:
                eastMoves.add(e)
                eastDests.add(dest)
        eastCukes = eastCukes.difference(eastMoves).union(eastDests)

        southMoves = set()
        southDests = set()
        for s in southCukes:
            dest = (s[0], (s[1] + 1) % h)
            if dest not in eastCukes and dest not in southCukes:
                southMoves.add(s)
                southDests.add(dest)
        southCukes = southCukes.difference(southMoves).union(southDests)

        i += 1
        if len(eastMoves) + len(southMoves) == 0:
            break

    return i

def part2(output=False):
    return 'RemoteStart!'
