from collections import defaultdict
from itertools import combinations

from mrm.dsu import DisjointSetUnion
from mrm.parse import all_nums
import mrm.point as pt
from mrm.util import big_pi

def parse():
    with open('data/aoc_2025/08.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [tuple(all_nums(l)) for l in lines]

def get_dists(j_boxes):
    return sorted((pt.dist(a, b), a, b) for a, b in combinations(j_boxes, 2))

def part1(output=False):
    j_boxes = parse()
    dists = get_dists(j_boxes)

    dsu = DisjointSetUnion()
    dsu.add_nodes(j_boxes)
    for d in dists[:1000]:
        _, box_1, box_2 = d
        dsu.union(box_1, box_2)

    cmp_sizes = sorted((len(s) for s in dsu.sets().values()), reverse=True)
    if output:
        print('Top 25 component sizes:', cmp_sizes[:25])

    return big_pi(cmp_sizes[:3])

def part2(output=False):
    j_boxes = parse()
    max_edges = len(j_boxes) - 1
    dists = iter(get_dists(j_boxes))

    dsu = DisjointSetUnion()
    dsu.add_nodes(j_boxes)
    edge_cnt = 0
    while edge_cnt < max_edges:
        _, box_1, box_2 = next(dists)
        if dsu.union(box_1, box_2):
            edge_cnt += 1
    return box_1[0] * box_2[0]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
