from itertools import product
from functools import reduce

with open('data/aoc_2020/17.txt') as f:
    dat = [x.strip() for x in f.readlines()]

blocks = set()
for y, d in enumerate(dat):
    for x, c in enumerate(d):
        if c == '#':
            blocks.add((x, y, 0, 0))

def active_neigh(blocks, block):
    active = 0
    x, y, z, w = block
    for dx, dy, dz in product([-1, 0, 1], repeat=3):
        if dx == 0 and dy == 0 and dz == 0:
            continue
        if (x + dx, y + dy, z + dz, w) in blocks:
            active += 1

    return active

def active_neigh_4d(blocks, block):
    active = 0
    x, y, z, w = block
    for dx, dy, dz, dw in product([-1, 0, 1], repeat=4):
        if dx == 0 and dy == 0 and dz == 0 and dw == 0:
            continue
        if (x + dx, y + dy, z + dz, w + dw) in blocks:
            active += 1

    return active

def set_range(blocks):
    min_vals = reduce(lambda a, b: (min(a[0], b[0]), min(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])), blocks)
    max_vals = reduce(lambda a, b: (max(a[0], b[0]), max(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])), blocks)

    return [min_vals, max_vals]

def part1(output=False):
    p1b = set(blocks)
    
    for i in range(6):
        new_inactive = set()
        for b in p1b:
            n = active_neigh(p1b, b)
            if n < 2 or n > 3:
                new_inactive.add(b)
        
        new_active = set()
        r = set_range(p1b)
        for z in range(r[0][2]-1, r[1][2]+2):
            for y in range(r[0][1]-1, r[1][1]+2):
                for x in range(r[0][0]-1, r[1][0]+2):
                    if (x, y, z, 0) not in p1b and active_neigh(p1b, (x, y, z, 0)) == 3:
                        new_active.add((x, y, z, 0))

        p1b = p1b.difference(new_inactive).union(new_active)

    return len(p1b)

def part2(output=False):
    p2b = set(blocks)
    
    for i in range(6):
        new_inactive = set()
        for b in p2b:
            n = active_neigh_4d(p2b, b)
            if n < 2 or n > 3:
                new_inactive.add(b)
        
        new_active = set()
        r = set_range(p2b)
        for w in range(r[0][3]-1, r[1][3]+2):
            for z in range(r[0][2]-1, r[1][2]+2):
                for y in range(r[0][1]-1, r[1][1]+2):
                    for x in range(r[0][0]-1, r[1][0]+2):
                        if (x, y, z, w) not in p2b and active_neigh_4d(p2b, (x, y, z, w)) == 3:
                            new_active.add((x, y, z, w))

        p2b = p2b.difference(new_inactive).union(new_active)

    return len(p2b)
