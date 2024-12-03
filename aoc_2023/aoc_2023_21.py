from functools import cache
from collections import deque
from mrm.point import adj_ortho

with open('data/aoc_2023/21.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    width = len(dat[0])
    height = len(dat)

def parse():
    garden_areas = {}
    start = None
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            if c in '.S':
                garden_areas[(x, y)] = True
                if c == 'S':
                    start = (x, y)

    return garden_areas, start

gardens, start_pt = parse()

def make_adj():
    adj = {}
    for g in gardens:
        adj[g] = adj_ortho(g, gardens)
    return adj

def run_to_dist(dist, adj_fn, start = start_pt):
    explore = deque([(start, 0)])
    seen = set()
    at_dist = set()
    while len(explore) != 0:
        pt, wt = explore.pop()
        seen.add((pt, wt))
        if wt == dist:
            at_dist.add(pt)
            continue
        for a in adj_fn(pt):
            npt = (a, wt + 1)
            if npt not in seen:
                explore.append((a, wt + 1))

    return at_dist

def part1(output = True):
    adj = make_adj()
    at_64 = run_to_dist(64, adj.get)

    if output:
        print('Start:', start_pt)
        for y in range(len(dat)):
            for x in range(len(dat[0])):
                if (x, y) not in gardens:
                    print('#', end='')
                else:
                    print('o' if (x,y) in at_64 else '.', end='')
            print()

    return len(at_64)

@cache
def adj_ortho_tiled(pt):
    x, y = pt
    adj = [(x-1, y), (x+1,y), (x,y-1), (x,y+1)]
    res = []
    for a in adj:
        ax, ay = a
        ma = (ax % width, ay % height)
        if a in gardens or ma in gardens:
            res += [a]
    return res

def part2(output = True):
    # 65 gets to the center of the edges adjacent tiles
    # Then 131 fully crosses those tiles
    # Any tile around for 131+65 is fully explored
    # Expanding diamond pattern since exploring in all 4 directions
    # Try quadratic growth

    r1 = len(run_to_dist(start_pt[0], adj_ortho_tiled))
    if output:
        print(start_pt[0], r1)

    r2 = len(run_to_dist(start_pt[0] + width, adj_ortho_tiled))
    if output:
        print(start_pt[0] + width, r2)

    r3 = len(run_to_dist(start_pt[0] + 2 * width, adj_ortho_tiled))
    if output:
        print(start_pt[0] + 2 * width, r3)

    a = r1
    b = (4 * r2 - r3 - 3 * r1) // 2
    c = r2 - a - b

    rep = (26501365 - 65) // width

    if output:
        print(a, b, c)
        print(rep)

    return a + rep * b + rep * rep * c

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
