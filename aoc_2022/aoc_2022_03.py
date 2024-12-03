from mrm.iter import batched

def parse():
    with open('data/aoc_2022/03.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def priority(item):
    if item >= 'a' and item <= 'z':
        return ord(item)-ord('a')+1
    if item >= 'A' and item <= 'Z':
        return ord(item)-ord('A')+27
    print("PANIC!")

def part1(output=False):
    lines = parse()
    score = 0
    for l in lines:
        gotmatch = 0
        s=len(l)
        p=int(s/2)

        gotmatch = (set(l[0:p]) & set(l[p:s])).pop()

        if output:
            print(gotmatch, 'in', l)
        score += priority(gotmatch)

    return score

def part2(output=False):
    lines = parse()
    score = 0
    group = []
    c = 0
    for group in batched(lines, 3):
        gotmatch = (set(group[0]) & set(group[1]) & set(group[2])).pop()
        if output:
            print(gotmatch, 'in', group)
        score += priority(gotmatch)
    
    return score
