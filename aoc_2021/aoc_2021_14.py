import re

with open('data/aoc_2021/14.txt') as f:
    dat = [x.strip() for x in f.readlines()]
r = re.compile('([A-Z]{2}) -> ([A-Z])')
subs = {a: b for (a,b) in [r.match(l).groups() for l in dat[2:]]}
pairs = subs.keys()
genmap = {p: [f'{p[0]}{subs[p]}', f'{subs[p]}{p[1]}'] for p in pairs}
letters = set([x for p in pairs for x in p])

def part1(output=False):
    polymer = dat[0]
    cnts = {p: 0 for p in pairs}
    for i in range(len(polymer)-1):
        cnts[polymer[i:i+2]] += 1
        
    for i in range(10):
        addCnts = {p: 0 for p in pairs}
        for p in [k for k in cnts.keys() if cnts[k] != 0]:
            addCnts[p] -= cnts[p]
            for g in genmap[p]:
                addCnts[g] += cnts[p]
        for k, v in addCnts.items():
            cnts[k] += v
    singleCnts = {l: 0 for l in letters}

    for p in cnts.keys():
        singleCnts[p[0]] += cnts[p]
        singleCnts[p[1]] += cnts[p]

    singleCnts[polymer[0]] -= 1
    singleCnts[polymer[-1]] -= 1

    for l in letters:
        singleCnts[l] = int(singleCnts[l] / 2)

    singleCnts[polymer[0]] += 1
    singleCnts[polymer[-1]] += 1
        
    srtcnts = sorted(singleCnts.items(), key=lambda x: x[1])
    ans1 = srtcnts[-1][1] - srtcnts[0][1]
    return ans1

def part2(output=False):
    polymer = dat[0]
    cnts = {p: 0 for p in pairs}
    for i in range(len(polymer)-1):
        cnts[polymer[i:i+2]] += 1
        
    for i in range(40):
        addCnts = {p: 0 for p in pairs}
        for p in [k for k in cnts.keys() if cnts[k] != 0]:
            addCnts[p] -= cnts[p]
            for g in genmap[p]:
                addCnts[g] += cnts[p]
        for k, v in addCnts.items():
            cnts[k] += v

    singleCnts = {l: 0 for l in letters}

    for p in cnts.keys():
        singleCnts[p[0]] += cnts[p]
        singleCnts[p[1]] += cnts[p]

    singleCnts[polymer[0]] -= 1
    singleCnts[polymer[-1]] -= 1

    for l in letters:
        singleCnts[l] = int(singleCnts[l] / 2)

    singleCnts[polymer[0]] += 1
    singleCnts[polymer[-1]] += 1
        
    srtcnts = sorted(singleCnts.items(), key=lambda x: x[1])
    ans2 = srtcnts[-1][1] - srtcnts[0][1]
    return ans2

