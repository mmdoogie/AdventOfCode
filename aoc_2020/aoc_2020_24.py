with open('data/aoc_2020/24.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def compute_blackTiles():
    blackTiles = set()
    for d in dat:
        x, y = 0, 0
        diag = False
        for c in d:
            if c == 'e':
                if diag:
                    x += 1
                else:
                    x += 2
                diag = False
            elif c == 'w':
                if diag:
                    x -= 1
                else:
                    x -= 2
                diag = False
            elif c == 'n':
                y -= 2
                diag = True
            elif c == 's':
                y += 2
                diag = True
        if (x, y) in blackTiles:
            blackTiles.remove((x, y))
        else:
            blackTiles.add((x, y))
    return blackTiles

def part1(output=False):
    blackTiles = compute_blackTiles()
    return len(blackTiles)

def hexneigh(loc):
    x, y = loc
    neigh = set([(x - 2, y), (x + 2, y), (x - 1, y - 2), (x - 1, y + 2), (x + 1, y - 2), (x + 1, y + 2)])
    return neigh

def whiteTiles(blackTiles):
    allTiles = set()
    for b in blackTiles:
        allTiles = allTiles.union(hexneigh(b))
    return allTiles.difference(blackTiles)

def part2(output=False):
    blackTiles = compute_blackTiles()
    for day in range(100):
        wt = whiteTiles(blackTiles)
        addBlack = set()
        for w in wt:
            neigh = sum([n in blackTiles for n in hexneigh(w)])
            if neigh == 2:
                addBlack.add(w)

        addWhite = set()
        for b in blackTiles:
            neigh = sum([n in blackTiles for n in hexneigh(b)])
            if neigh == 0 or neigh > 2:
                addWhite.add(b)

        blackTiles = blackTiles.difference(addWhite).union(addBlack)
    return len(blackTiles)
