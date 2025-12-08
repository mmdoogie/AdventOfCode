from collections import defaultdict
from itertools import combinations

from mrm.graph import connected_component
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
    ngh = defaultdict(list)
    for d in dists[:1000]:
        _, box_1, box_2 = d
        ngh[box_1] += [box_2]
        ngh[box_2] += [box_1]

    cmp_sizes = []
    left = set(j_boxes)
    while left:
        at_box = left.pop()
        cc = connected_component(ngh, at_box)
        cmp_sizes += [len(cc)]
        left -= cc

    cmp_sizes.sort(reverse=True)
    if output:
        print('Top 25 component sizes:', cmp_sizes[:25])
    return big_pi(cmp_sizes[:3])

def part2(output=False):
    j_boxes = parse()

    dists = get_dists(j_boxes)
    ngh = defaultdict(list)
    chk_box = j_boxes[0]
    unlinked = set(j_boxes)
    for i, d in enumerate(dists):
        _, box_1, box_2 = d
        ngh[box_1] += [box_2]
        ngh[box_2] += [box_1]
        if unlinked:
            unlinked.discard(box_1)
            unlinked.discard(box_2)
            chk_box = box_1
            continue
        cc = connected_component(ngh, chk_box)
        if len(cc) == len(j_boxes):
            if output:
                print(f'{i + 1} total connections')
            return box_1[0] * box_2[0]
        if len(cc) > len(j_boxes) // 2:
            remain = set(j_boxes).difference(cc)
            chk_box = remain.pop()
            if output:
                print(f'{i + 1} connections, moving cc check to {chk_box}, cc size {len(cc)}')

    return ''

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
