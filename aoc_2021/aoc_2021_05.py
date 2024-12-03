import re
import itertools

with open('data/aoc_2021/05.txt', 'r') as f:
    dat = f.readlines()
pat = re.compile(r'(\d*),(\d*) -> (\d*),(\d*)')
lines = [[int(v) for v in pat.match(x.strip()).groups()] for x in dat]

hmap = dict()
vmap = dict()

for l in lines:
    if l[1] == l[3]:
        if l[1] in hmap:
            hmap[l[1]] += [(min(l[0], l[2]), max(l[0], l[2]))]
        else:
            hmap[l[1]]  = [(min(l[0], l[2]), max(l[0], l[2]))]
            
    if l[0] == l[2]:
        if l[0] in vmap:
            vmap[l[0]] += [(min(l[1], l[3]), max(l[1], l[3]))]
        else:
            vmap[l[0]]  = [(min(l[1], l[3]), max(l[1], l[3]))]

def part1(output=False):
    overlaps = set()

    for row, s in hmap.items():
        pairs = itertools.combinations(s, 2)
        for p in pairs:
            if p[0][0] < p[1][0]:
                left = p[0]
                right = p[1]
            else:
                left = p[1]
                right = p[0]

            if right[0] >= left[0] and right[0] <= left[1]:
                minval = right[0]

                if left[1] <= right[1]:
                    maxval = left[1]
                else:
                    maxval = right[1]

                for x in range(minval, maxval + 1):
                    overlaps.add((x, row))

    for col, s in vmap.items():
        for g in s:
            for y in range(g[0], g[1] + 1):
                if y in hmap:
                    for h in hmap[y]:
                        if col >= h[0] and col <= h[1]:
                            overlaps.add((col, y))

    for col, s in vmap.items():
        pairs = itertools.combinations(s, 2)
        for p in pairs:
            if p[0][0] < p[1][0]:
                left = p[0]
                right = p[1]
            else:
                left = p[1]
                right = p[0]
            
            if right[0] >= left[0] and right[0] <= left[1]:
                minval = right[0]

                if left[1] <= right[1]:
                    maxval = left[1]
                else:
                    maxval = right[1]

                for y in range(minval, maxval + 1):
                    overlaps.add((col, y))

    return len(overlaps)

def part2(output=False):
    hits = dict()

    for l in lines:
        if l[0] == l[2]:
            for y in range(min(l[1],l[3]), max(l[1],l[3])+1):
                if (l[0], y) in hits:
                    hits[(l[0], y)] += 1
                else:
                    hits[(l[0], y)] = 1
        elif l[1] == l[3]:
            for x in range(min(l[0],l[2]), max(l[0],l[2])+1):
                if (x, l[1]) in hits:
                    hits[(x, l[1])] += 1
                else:
                    hits[(x, l[1])] = 1
        else:
            if l[0] < l[2]:
                sx, sy = l[0], l[1]
                cx = l[2]-l[0]+1
                dx, dy = 1, 1 if l[3] > l[1] else -1
            else:
                sx, sy = l[2], l[3]
                cx = l[0]-l[2]+1
                dx, dy = 1, 1 if l[1] > l[3] else -1
            for i in range(cx):
                p = (sx+i*dx, sy+i*dy)
                if p in hits:
                    hits[p] += 1
                else:
                    hits[p] = 1

    intersects = [h for h in hits.values() if h > 1]

    return len(intersects)
