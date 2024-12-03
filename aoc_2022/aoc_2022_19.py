from math import prod
import re

from tqdm import tqdm

def parse():
    with open('data/aoc_2022/19.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    rx = re.compile("Blueprint ([0-9]+).*ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.")
    blueprints = [list(map(int, rx.match(l).groups())) for l in lines]

    return blueprints

def part1(output=False):
    blueprints = parse()
    scores = []
    prog = None
    for bp in blueprints:
        maxScores = 0
        maxGeoPot = 0

        if output:
            print("New BP:", bp)
            if not prog:
                prog = tqdm(maxinterval=1, total=24, leave=False)
            prog.n = 0

        paths = [((0,0,0,0,1,0,0,0,24), "X")]
        tried = {}
        lastpl = 25
        while paths:
            p = paths.pop(0)
            tried[p] = True
            ore, clay, obsidian, geodes, oreBots, clayBots, obsidianBots, geodeBots, rt = p[0]
            act = p[1]
            if rt < lastpl:
                if output:
                    prog.update()
                    prog.refresh()
                lastpl = rt
                maxGeoPot = 0
            
            ore += oreBots
            clay += clayBots
            obsidian += obsidianBots
            geodes += geodeBots
            rt -= 1
        
            bpn, bpOre1, bpOre2, bpOre3, bpClay1, bpOre4, bpObs1 = bp
            if act == "O":
                oreBots += 1
                ore -= bpOre1
            elif act == "C":
                clayBots += 1
                ore -= bpOre2
            elif act == "S":
                obsidianBots += 1
                ore -= bpOre3
                clay -= bpClay1
            elif act == "G":
                geodeBots += 1
                ore -= bpOre4
                obsidian -= bpObs1

            s = (ore, clay, obsidian, geodes, oreBots, clayBots, obsidianBots, geodeBots, rt)
            
            if geodes > maxScores:
                maxScores = geodes
            if geodes < maxScores:
                continue
            if rt == 0:
                continue

            ts = rt*rt+rt/2
            clayPot = clay + rt*clayBots + ts
            obsPot = obsidian + rt*obsidianBots + ts
            geoPot = geodes + rt*geodeBots + ts
            if obsidianBots == 0 and clayPot < bpClay1:
                continue
            if obsidianBots == 0 and clayPot/bpClay1*rt < bpObs1:
                continue
            if geodeBots == 0 and obsPot < bpObs1:
                continue
            if geoPot > maxGeoPot:
                maxGeoPot = geoPot
            if geoPot < maxGeoPot:
                continue

            np = []
            blocked = False
            if ore >= bpOre4 and obsidian >= bpObs1:
                np += [(s, "G")]
                blocked = True
            if act != "s" and ore >= bpOre3 and clay >= bpClay1 and obsidianBots < bpObs1:
                np += [(s, "S")]
                if act not in "sco":
                    np += [(s, "s")]
                blocked = True
            if act != "c" and ore >= bpOre2 and clayBots < bpClay1:
                np += [(s, "C")]
                if act not in "sco":
                    np += [(s, "c")]
                blocked = True
            if act != "o" and ore >= bpOre1 and oreBots < max(bpOre1, bpOre2, bpOre3, bpOre4):
                np += [(s, "O")]
                if act not in "sco":
                    np += [(s, "o")]
                blocked = True
            if not blocked:
                if act in "sco":
                    np += [(s, act)]
                else:
                    np += [(s, "X")]

            for nnp in np:
                if nnp not in tried:
                    tried[nnp] = True
                    paths += [nnp]
        
        if output:
            print(f"BP {bp[0]} Score {maxScores}")
        scores += [maxScores]

    if output:
        prog.close()
    quals = [bp[0]*g for bp,g in zip(blueprints,scores)]
    if output:
        print(quals, sum(quals))

    return sum(quals)

def part2(output=False):
    blueprints = parse()
    scores = []
    prog = None
    for bp in blueprints[0:3]:
        maxScores = 0
        maxGeoPot = 0

        if output:
            print("New BP:", bp)
            if not prog:
                prog = tqdm(maxinterval=1, total=32, leave=False)
            prog.n = 0

        paths = [((0,0,0,0,1,0,0,0,32), "X")]
        tried = {}
        lastpl = 33
        while paths:
            p = paths.pop(0)
            tried[p] = True
            ore, clay, obsidian, geodes, oreBots, clayBots, obsidianBots, geodeBots, rt = p[0]
            act = p[1]
            if rt < lastpl:
                if output:
                    prog.update()
                    prog.refresh()
                lastpl = rt
                maxGeoPot = 0
            
            ore += oreBots
            clay += clayBots
            obsidian += obsidianBots
            geodes += geodeBots
            rt -= 1
        
            bpn, bpOre1, bpOre2, bpOre3, bpClay1, bpOre4, bpObs1 = bp
            if act == "O":
                oreBots += 1
                ore -= bpOre1
            elif act == "C":
                clayBots += 1
                ore -= bpOre2
            elif act == "S":
                obsidianBots += 1
                ore -= bpOre3
                clay -= bpClay1
            elif act == "G":
                geodeBots += 1
                ore -= bpOre4
                obsidian -= bpObs1

            s = (ore, clay, obsidian, geodes, oreBots, clayBots, obsidianBots, geodeBots, rt)
            
            if geodes > maxScores:
                maxScores = geodes
            if geodes < maxScores:
                continue
            if rt == 0:
                continue

            ts = rt*rt+rt/2
            clayPot = clay + rt*clayBots + ts
            obsPot = obsidian + rt*obsidianBots + ts
            geoPot = geodes + rt*geodeBots + ts
            if obsidianBots == 0 and clayPot < bpClay1:
                continue
            if obsidianBots == 0 and clayPot/bpClay1*rt < bpObs1:
                continue
            if geodeBots == 0 and obsPot < bpObs1:
                continue
            if geoPot > maxGeoPot:
                maxGeoPot = geoPot
            if geoPot < maxGeoPot:
                continue

            np = []
            blocked = False
            if ore >= bpOre4 and obsidian >= bpObs1:
                np += [(s, "G")]
                blocked = True
            if act != "s" and ore >= bpOre3 and clay >= bpClay1 and obsidianBots < bpObs1:
                np += [(s, "S")]
                if act not in "sco":
                    np += [(s, "s")]
                blocked = True
            if act != "c" and ore >= bpOre2 and clayBots < bpClay1:
                np += [(s, "C")]
                if act not in "sco":
                    np += [(s, "c")]
                blocked = True
            if act != "o" and ore >= bpOre1 and oreBots < max(bpOre1, bpOre2, bpOre3, bpOre4):
                np += [(s, "O")]
                if act not in "sco":
                    np += [(s, "o")]
                blocked = True
            if not blocked:
                if act in "sco":
                    np += [(s, act)]
                else:
                    np += [(s, "X")]

            for nnp in np:
                if nnp not in tried:
                    tried[nnp] = True
                    paths += [nnp]
        
        if output:
            print(f"BP {bp[0]} Score {maxScores}")
        scores += [maxScores]

    if output:
        prog.close()
        print(scores, prod(scores))

    return prod(scores)
