from collections import defaultdict

def parse():
    with open('data/aoc_2024/23.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    pairs = [l.split('-') for l in lines]
    conns = defaultdict(set)
    for a, b in pairs:
        conns[a].add(b)
        conns[b].add(a)
    return conns

def part1(output=False):
    conns = parse()

    groups = set()
    for pc_1 in conns:
        if not pc_1.startswith('t'):
            continue
        for pc_2 in conns[pc_1]:
            for pc_3 in conns[pc_2]:
                if pc_1 in conns[pc_3]:
                    groups.add(tuple(sorted([pc_1, pc_2, pc_3])))

    return len(groups)

def part2(output=False):
    conns = parse()

    max_comp = []
    remain = set(conns)
    curr_comp = set([remain.pop()])
    while remain:
        to_add = set()
        for c in curr_comp:
            for n in conns[c]:
                if n in curr_comp or n in to_add:
                    continue
                if all(cc in conns[n] for cc in curr_comp | to_add):
                    to_add.add(n)
        curr_comp |= to_add
        remain -= to_add
        if not to_add:
            if len(curr_comp) > len(max_comp):
                max_comp = curr_comp
            curr_comp = set([remain.pop()])

    return ','.join(sorted(max_comp))

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
