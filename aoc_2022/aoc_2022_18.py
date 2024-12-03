def parse():
    with open('data/aoc_2022/18.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()
    cubes = [tuple(map(int,l.split(","))) for l in lines]

    allFaces = 0
    for c in cubes:
        faces = 6
        if (c[0]+1,c[1],c[2]) in cubes:
            faces -= 1
        if (c[0]-1,c[1],c[2]) in cubes:
            faces -= 1
        if (c[0],c[1]+1,c[2]) in cubes:
            faces -= 1
        if (c[0],c[1]-1,c[2]) in cubes:
            faces -= 1
        if (c[0],c[1],c[2]+1) in cubes:
            faces -= 1
        if (c[0],c[1],c[2]-1) in cubes:
            faces -= 1
        allFaces += faces

    return allFaces

def part2(output=False):
    lines = parse()
    cubes = [tuple(map(int,l.split(","))) for l in lines]
    minX = min([c[0] for c in cubes])
    minY = min([c[1] for c in cubes])
    minZ = min([c[2] for c in cubes])
    maxX = max([c[0] for c in cubes])
    maxY = max([c[1] for c in cubes])
    maxZ = max([c[2] for c in cubes])

    dirs = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]
    visited = []
    boundary = []

    nextPoints = [(minX-1, minY-1, minZ-1)]
    while nextPoints:
        moreNextPoints = []
        for pt in nextPoints:
            visited += [pt]
            for d in dirs:
                loc = (pt[0]+d[0], pt[1]+d[1], pt[2]+d[2])
                if loc in visited or loc[0] < minX-1 or loc[0] > maxX+1 or loc[1] < minY-1 or loc[1] > maxY+1 or loc[2] < minZ-1 or loc[2] > maxZ+1:
                    continue
                if loc in cubes:
                    boundary += [loc]
                    continue
                if loc not in moreNextPoints:
                    moreNextPoints += [loc]
        if output:
            print("Visited", len(visited), "Boundary", len(boundary), "Exploring", len(moreNextPoints))
        nextPoints = moreNextPoints

    for y in range(minY, maxY+1):
        o = "| "
        for z in range(minZ, maxZ+1, 3):
            l = ["."]*20
            for x in range(minX, maxX+1):
                p = (x,y,z)
                if p in boundary:
                    l[x] = chr(ord("0") + sum([1 for x in boundary if x == p]))
                elif p in cubes:
                    l[x] = "*"
            o += ''.join(l) + " | "
        if output:
            print(o)
    if output:
        l = "| "
        for z in range(minZ, maxZ+1, 3):
            c = f"Z = {z}"
            l += c + " "*(20-len(c)) + " | "
        print(l)

    return len(boundary)
