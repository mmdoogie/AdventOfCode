import re
import itertools

def parse():
    with open('data/aoc_2022/16.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    allValves = {}
    rx = re.compile("Valve ([A-Z]{2}) .*=([0-9]+); .*valve[s]? ([A-Z, ]+)")
    for l in lines:
        g = rx.search(l)
        name = g[1]
        rate = int(g[2])
        dests = g[3].split(", ")
        allValves[name] = {"rate": rate, "dest": dests, "dist": 1000, "visited": False}
    allDist = {}
    for k,v in allValves.items():
        if v["rate"] == 0 and k != "AA":
            continue
        allDist[k] = doDistancing(allValves, k)

    return allValves, allDist

def doDistancing(valves, startPos):
    for k,v in valves.items():
        v["dist"] = 1000
        v["visited"] = False
    valves[startPos]["dist"] = 0

    currPos = startPos
    while True:
        newDist = valves[currPos]["dist"] + 1
        for n in valves[currPos]["dest"]:
            if valves[n]["visited"]:
                continue
            valves[n]["dist"] = min(valves[n]["dist"], newDist)

        valves[currPos]["visited"] = True
        rem = sorted([(k, v["dist"]) for k,v in valves.items() if not v["visited"] and v["dist"] < 1000], key=lambda x: x[1])
        if not rem:
            break
        nextPos, minDist = rem[0]
        currPos = nextPos

    dists = []
    for k,v in valves.items():
        if v["rate"] == 0 or k == startPos:
            continue
        dists += [(k, v["dist"], v["rate"])]

    return dists

def part1(output=False):
    allValves, allDist = parse()

    ptfs = [(["AA"], 30, 0)]
    while True:
        newPtfs = []
        for p, t, f in ptfs:
            valves = allDist[p[-1]]
            choices = [(v[0], t - v[1] - 1, v[2]) for v in valves if t - v[1] > 1 and v[0] not in p]
            for c in choices:
                newPtfs += [(p + [c[0]], c[1], f + c[1] * c[2])]
        if not newPtfs:
            break
        prevPtfs = ptfs
        ptfs = newPtfs

    ptfs.sort(key=lambda x: x[2], reverse=True)
    return ptfs[0][2]

def part2(output=False):
    allValves, allDist = parse()

    ptfs = [(["AA"], 26, 0)]
    while True:
        newPtfs = []
        for p, t, f in ptfs:
            valves = allDist[p[-1]]
            choices = [(v[0], t - v[1] - 1, v[2]) for v in valves if t - v[1] > 1 and v[0] not in p]
            for c in choices:
                newPtfs += [(p + [c[0]], c[1], f + c[1] * c[2])]
        if not newPtfs:
            break
        prevPtfs = ptfs
        ptfs = newPtfs

    rs = []
    for ptf in prevPtfs + ptfs:
        rs += [(set(ptf[0][1:]), ptf[2])]

    fmax = 0
    for pfm, pfe in itertools.product(rs, rs):
        if pfm[0] & pfe[0]:
            continue
        if pfm[1] + pfe[1] > fmax:
            fmax = pfm[1] + pfe[1]

    return fmax
