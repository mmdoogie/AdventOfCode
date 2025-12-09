from collections import defaultdict
from itertools import combinations, pairwise

from mrm.parse import all_nums

def parse():
    with open('data/aoc_2025/09.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    pts = [tuple(all_nums(l)) for l in lines]
    return pts

def rect_area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

def part1(output=False):
    pts = parse()
    max_area = max(rect_area(*pp) for pp in combinations(pts, 2))
    return max_area

def make_edges(pts):
    h_edges = defaultdict(list)
    v_edges = defaultdict(list)
    for p1, p2 in pairwise(pts + [pts[0]]):
        if p1[0] != p2[0]:
            h_edges[p1[1]] += [(min(p1[0], p2[0]), max(p1[0], p2[0]))]
        else:
            v_edges[p1[0]] += [(min(p1[1], p2[1]), max(p1[1], p2[1]))]
    return h_edges, v_edges

def raycast(v_edges, ctr_x, ctr_y):
    inside = False
    for x in v_edges:
        if x >= ctr_x:
            continue
        for r in v_edges[x]:
            if r[0] <= ctr_y <= r[1]:
                inside = not inside
                break
    return inside

def intersect_vert(v_edges, min_x, max_x, min_y, max_y):
    for x in v_edges:
        if x <= min_x or x >= max_x:
            continue
        for r in v_edges[x]:
            if r[1] > min_y and r[0] < max_y:
                return True
    return False

def intersect_horiz(h_edges, min_x, max_x, min_y, max_y):
    for y in h_edges:
        if y <= min_y or y >= max_y:
            continue
        for r in h_edges[y]:
            if r[1] > min_x and r[0] < max_x:
                return True
    return False

def part2(output=False):
    pts = parse()
    h_edges, v_edges = make_edges(pts)

    max_area = 0
    for a, b in combinations(pts, 2):
        min_x = min(a[0], b[0])
        max_x = max(a[0], b[0])
        min_y = min(a[1], b[1])
        max_y = max(a[1], b[1])

        if intersect_vert(v_edges, min_x, max_x, min_y, max_y):
            continue

        if intersect_horiz(h_edges, min_x, max_x, min_y, max_y):
            continue

        ctr_x = (min_x + max_x) // 2
        ctr_y = (min_y + max_y) // 2
        if not raycast(v_edges, ctr_x, ctr_y):
            continue

        area = rect_area(a, b)
        if area > max_area:
            max_area = area
            if output:
                print(a, b, area)

    return max_area

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
