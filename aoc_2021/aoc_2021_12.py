with open('data/aoc_2021/12.txt') as f:
    dat = [x.strip() for x in f.readlines()]

cavemap = dict()
for line in dat:
    lhs, rhs = line.split('-')
    if rhs != 'start' and lhs != 'end':
        if lhs in cavemap:
            cavemap[lhs] += [rhs]
        else:
            cavemap[lhs] = [rhs]
    if lhs != 'start' and rhs != 'end':
        if rhs in cavemap:
            cavemap[rhs] += [lhs]
        else:
            cavemap[rhs] = [lhs]

def part1(output=False):
    fullPaths = []
    explorePaths = [['start']]
    while len(explorePaths) > 0:
        currPath = explorePaths.pop()
        for exit in cavemap[currPath[-1]]:
            if exit[0] >= 'a' and exit[0] <= 'z' and exit in currPath:
                continue
            if exit == 'end':
                fullPaths += [currPath + ['end']]
                continue
            if len(currPath) > 20:
                continue
            explorePaths += [currPath + [exit]]

    pathStrs = ['-'.join(x) for x in fullPaths]
    validPathCount = len(set(pathStrs))
    return validPathCount

def part2(output=False):
    fullPaths = []
    explorePaths = [['start']]
    while len(explorePaths) > 0:
        currPath = explorePaths.pop()
        for exit in cavemap[currPath[-1]]:
            if exit[0] >= 'a' and exit[0] <= 'z' and exit in currPath:
                skip = False
                smallCaves = [x for x in currPath if x[0] >= 'a' and x[0] <= 'z']
                for sc in set(smallCaves):
                    if len([x for x in currPath if x == sc]) == 2:
                        skip = True
                        break
                if not skip:
                    explorePaths += [currPath + [exit]]
                continue
            if exit == 'end':
                fullPaths += [currPath + ['end']]
                continue
            if len(currPath) > 20:
                continue
            explorePaths += [currPath + [exit]]

    pathStrs = ['-'.join(x) for x in fullPaths]
    validPathCount = len(set(pathStrs))
    return validPathCount
