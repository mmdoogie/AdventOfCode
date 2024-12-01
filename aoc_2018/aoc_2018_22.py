from collections import defaultdict
from functools import cache

from mrm.dijkstra import dijkstra, Dictlike

with open('data/aoc_2018/22.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

@cache
def erosion_level(loc, tgt, depth):
    x, y = loc
    if x == 0 and y == 0:
        geo_index = 0
    elif loc == tgt:
        geo_index = 0
    elif y == 0:
        geo_index = x * 16807
    elif x == 0:
        geo_index = y * 48271
    else:
        geo_index = erosion_level((x - 1, y), tgt, depth) * erosion_level((x, y - 1), tgt, depth)

    return (geo_index + depth) % 20183

def part1(output = True):
    depth = int(dat[0].split(': ')[1])
    target = tuple(int(x) for x in dat[1].split(': ')[1].split(','))

    if output:
        print(f'Depth: {depth}')
        print(f'Target: {target}')

    return sum(erosion_level((x, y), target, depth) % 3 for x in range(target[0] + 1) for y in range(target[1] + 1))

def part2(output = True):
    depth = int(dat[0].split(': ')[1])
    target = tuple(int(x) for x in dat[1].split(': ')[1].split(','))

    tools = {0: ['gear', 'torch'], 1: ['gear', 'neither'], 2: ['torch', 'neither']}

    def loc_tools(loc):
        return tools[erosion_level(loc, target, depth) % 3]

    @cache
    def neighbors(loc):
        x, y, pt = loc
        if x < 0 or y < 0:
            return []
        ngh = []
        p_tools = loc_tools((x, y))
        for ot in p_tools:
            if ot != pt:
                ngh += [(x, y, ot)]
        adj = [a for a in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if a[0] >= 0 and a[1] >= 0]
        for a in adj:
            if pt in loc_tools(a):
                ngh += [(*a, pt)]
        return ngh

    def est(pt):
        return abs(pt[0] - target[0]) + abs(pt[1] - target[1])

    def weight(pair):
        p1, p2 = pair

        if p1[2] == p2[2]:
            return 1

        return 7

    start_point = (0, 0, 'torch')
    end_point = (*target, 'torch')
    neighbors_dict = Dictlike(neighbors, lambda loc: loc[0] >= 0 and loc[1] >= 0)
    weights_dict = Dictlike(weight)

    weights = dijkstra(neighbors_dict, weights_dict, start_point, end_point, keep_paths = False, dist_est = est)

    return weights[end_point]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
