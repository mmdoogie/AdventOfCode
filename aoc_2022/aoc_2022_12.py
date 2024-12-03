import mrm.ansi_term as ansi

def parse():
    with open('data/aoc_2022/12.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()

    hmap = []

    for n,l in enumerate(lines):
        h = [ord(x)-ord('a') for x in list(l)]
        hmap += [h]
        if -14 in h: #S
            startPos = (h.index(-14), n)
            h[h.index(-14)] = 0
        if -28 in h: #E
            endPos = (h.index(-28), n)
            h[h.index(-28)] = 25\

    nodePos = []
    nodeDist = []
    nodeVisited = []
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            nodePos += [(x,y)]
            nodeDist += [int(10e6)]
            nodeVisited += [False]

    nodeDist[nodePos.index(startPos)] = 0

    maxX = len(lines[0])-1
    maxY = len(lines)-1
    currPos = startPos

    while True:
        neighbors = []
        if currPos[0] > 0:
            neighbors += [(currPos[0]-1, currPos[1])]
        if currPos[0] < maxX-1:
            neighbors += [(currPos[0]+1, currPos[1])]
        if currPos[1] > 0:
            neighbors += [(currPos[0], currPos[1]-1)]
        if currPos[1] < maxY-1:
            neighbors += [(currPos[0], currPos[1]+1)]

        for n in neighbors:
            if nodeVisited[nodePos.index(n)]:
                continue
            dh = hmap[n[1]][n[0]] - hmap[currPos[1]][currPos[0]]
            if dh <= 1:
                newDist = nodeDist[nodePos.index(currPos)] + 1
                if newDist < nodeDist[nodePos.index(n)]:
                    nodeDist[nodePos.index(n)] = newDist

        nodeVisited[nodePos.index(currPos)] = True
        if currPos == endPos:
            break

        remDist = min([x for n,x in enumerate(nodeDist) if not nodeVisited[n]])
        if remDist == int(10e6):
            break

        currPos = [x for n,x in enumerate(nodePos) if not nodeVisited[n] and nodeDist[n] == remDist][0]

    if currPos == endPos:
        return nodeDist[nodePos.index(endPos)]

def part2(output=False):
    lines = parse()

    starts = [(0,y) for y in range(len(lines))]

    hmap = []

    for n,l in enumerate(lines):
        h = [ord(x)-ord('a') for x in list(l)]
        hmap += [h]
        if -14 in h: #S
            #startPos = (h.index(-14), n)
            h[h.index(-14)] = 0
        if -28 in h: #E
            #endPos = (h.index(-28), n)
            startPos = (h.index(-28), n)
            h[h.index(-28)] = 25

    nodePos = []
    nodeDist = []
    nodeVisited = []
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            nodePos += [(x,y)]
            nodeDist += [int(10e6)]
            nodeVisited += [False]

    nodeDist[nodePos.index(startPos)] = 0

    maxX = len(lines[0])-1
    maxY = len(lines)-1
    currPos = startPos

    while True:
        neighbors = []
        if currPos[0] > 0:
            neighbors += [(currPos[0]-1, currPos[1])]
        if currPos[0] < maxX-1:
            neighbors += [(currPos[0]+1, currPos[1])]
        if currPos[1] > 0:
            neighbors += [(currPos[0], currPos[1]-1)]
        if currPos[1] < maxY-1:
            neighbors += [(currPos[0], currPos[1]+1)]

        for n in neighbors:
            if nodeVisited[nodePos.index(n)]:
                continue
            dh = hmap[n[1]][n[0]] - hmap[currPos[1]][currPos[0]]
            if dh >= -1:
                newDist = nodeDist[nodePos.index(currPos)] + 1
                if newDist < nodeDist[nodePos.index(n)]:
                    nodeDist[nodePos.index(n)] = newDist

        nodeVisited[nodePos.index(currPos)] = True

        remDist = [x for n,x in enumerate(nodeDist) if not nodeVisited[n]]
        minRem = min(remDist)
        if len(remDist) == 0 or minRem == int(10e6):
            break

        currPos = [x for n,x in enumerate(nodePos) if not nodeVisited[n] and nodeDist[n] == minRem][0]

    minDist = int(10e6)
    for n,p in enumerate(nodePos):
        if hmap[p[1]][p[0]] == 0:
            if nodeDist[n] < minDist:
                minDist = nodeDist[n]
                minNode = p

    if not output:
        return minDist

    print(minNode, minDist)

    currPos = minNode
    currDist = minDist
    hmap[currPos[1]][currPos[0]] += 1000

    while True:
        neighbors = []
        if currPos[0] > 0:
            neighbors += [(currPos[0]-1, currPos[1])]
        if currPos[0] < maxX-1:
            neighbors += [(currPos[0]+1, currPos[1])]
        if currPos[1] > 0:
            neighbors += [(currPos[0], currPos[1]-1)]
        if currPos[1] < maxY-1:
            neighbors += [(currPos[0], currPos[1]+1)]

        for n in neighbors:
            if nodeDist[nodePos.index(n)] == currDist - 1:
                currDist = currDist - 1
                currPos = n
                hmap[n[1]][n[0]] += 1000
        
        if currDist == 0:
            break;

    for y in range(len(lines)):
        l = ''
        for x in range(len(lines[0])):
            if hmap[y][x] >= 1000:
                l += ansi.red(chr(hmap[y][x] + ord('a') - 1000))
            else:
                l += chr(hmap[y][x] + ord('a'))
        print(l)

    return minDist
