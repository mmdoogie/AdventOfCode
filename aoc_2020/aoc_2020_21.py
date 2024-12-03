with open('data/aoc_2020/21.txt') as f:
    dat = [x.strip() for x in f.readlines()]

allIngrs = []
ingrs = {}
for d in dat:
    l, r = d.split(' (contains ')
    ing = set(l.split(' '))
    alr = r.strip(')').split(', ')
    allIngrs += ing
    
    for a in alr:
        if a not in ingrs:
            ingrs[a] = ing
        else:
            ingrs[a] = ingrs[a].intersection(ing)

def part1(output=False):
    cantBe = set(allIngrs)
    for k, v in ingrs.items():
        cantBe = cantBe.difference(v)

    cantOcc = 0
    for i in allIngrs:
        if i in cantBe:
            cantOcc += 1

    return cantOcc

def part2(output=False):
    while sum([len(x) for x in ingrs.values()]) != len(ingrs.keys()):
        for k, v in ingrs.items():
            if len(v) == 1:
                changed = False
                for k2, v2 in ingrs.items():
                    if k == k2:
                        continue
                    ingrs[k2] = v2.difference(v)

    order = sorted(ingrs.keys())
    cdil = ','.join([list(ingrs[k])[0] for k in order])

    return cdil
