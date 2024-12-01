from operator import eq, ge, le

with open('data/aoc_2015/16.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

analysis = {
    "children":    3,
    "cats":        7,
    "samoyeds":    2,
    "pomeranians": 3,
    "akitas":      0,
    "vizslas":     0,
    "goldfish":    5,
    "trees":       3,
    "cars":        2,
    "perfumes":    1
}

compare = {
    "cats":        ge,
    "trees":       ge,
    "pomeranians": le,
    "goldfish":    le,
    "children":    eq,
    "samoyeds":    eq,
    "akitas":      eq,
    "vizslas":     eq,
    "cars":        eq,
    "perfumes":    eq
}

def get_aunts_sue():
    sues = {}
    i = 1
    for d in dat:
        p = d.split(': ', 1)[1].split(', ')
        sue = {}
        for o in p:
            k, v = o.split(': ')
            sue[k] = int(v)
        sues[i] = sue
        i += 1
    return sues

def part1(output = True):
    sues = get_aunts_sue()

    remain = set(sues)
    remove = set()
    for s in remain:
        for p in sues[s]:
            if p in analysis and sues[s][p] != analysis[p]:
                remove.add(s)
    remain -= remove
    if len(remain) != 1:
        print('Error, too many matching Aunts Sue')

    return remain.pop()

def part2(output = True):
    sues = get_aunts_sue()

    remain = set(sues)
    remove = set([part1(False)])
    for s in remain:
        for p in sues[s]:
            if p in analysis and not compare[p](sues[s][p], analysis[p]):
                remove.add(s)
    remain -= remove
    if len(remain) != 1:
        print('Error, too many matching Aunts Sue', remain)

    return remain.pop()

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
