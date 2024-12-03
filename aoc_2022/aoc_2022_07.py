def parse():
    with open('data/aoc_2022/07.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def process(lines):
    files = []
    currPath = []
    for l in lines:
            p = l.strip().split(" ")
            if p[0] == "$":
                    if p[1] == "cd":
                            if p[2] == "/":
                                    continue
                            elif p[2] == "..":
                                    currPath.pop()
                                    continue
                            else:
                                    currPath = currPath + [p[2]]
                    elif p[1] == "ls":
                            continue
            else:
                    if p[0] == "dir":
                            files += [{"path": "/".join(currPath + [p[1]]), "name": "_", "size": 0}]
                    else:
                            files += [{"path": "/".join(currPath), "name": p[1], "size": int(p[0])}]

    allPaths = set([x["path"] for x in files])

    return files, allPaths

def part1(output=False):
    lines = parse()
    files, allPaths = process(lines)
    dirSizes = [{"path": p, "size":sum([f["size"] for f in files if f["path"].startswith(p)]) } for p in allPaths]
    smallTotal = sum([s["size"] for s in dirSizes if s["size"] <= 100000])
    return smallTotal

def part2(output=False):
    lines = parse()
    files, allPaths = process(lines)
    usedTotal = sum([f["size"] for f in files])
    freeSpace = 70000000 - usedTotal
    neededSpace = 30000000
    needToClear = neededSpace - freeSpace
    dirSizes = [{"path": p, "size":sum([f["size"] for f in files if f["path"].startswith(p)]) } for p in allPaths]
    deleteCandidates = [s for s in dirSizes if s["size"] >= needToClear]
    deleteCandidates = sorted(deleteCandidates, key=lambda x: x["size"])

    return deleteCandidates[0]["size"]
