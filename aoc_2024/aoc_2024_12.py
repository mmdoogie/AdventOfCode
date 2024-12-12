from functools import partial
from itertools import cycle, pairwise

from mrm.ansi_term import red, green, blue, cyan, magenta, yellow
from mrm.graph import connected_component
from mrm.image import print_image
import mrm.point as pt

def parse():
    with open('data/aoc_2024/12.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return pt.grid_as_dict(lines, with_inv = True)

colors = cycle([red, green, blue, cyan, magenta, yellow])
def component_highlighter(components, x, y, c):
    return components[(x, y)](c)

def part1(output=False):
    grid, inv = parse()
    ngh = {g: [a for a in pt.adj_ortho(g, grid) if a in inv[gv]] for g, gv in grid.items()}

    price = 0
    avail = set(grid)
    components = {}
    while avail:
        nodes = connected_component(ngh, avail.pop())
        area = len(nodes)
        perim = 4 * len(nodes) - sum(len(ngh[n]) for n in nodes)
        price += area * perim
        avail.difference_update(nodes)
        if output:
            curr_color = next(colors)
            components.update({n: curr_color for n in nodes})

    if output:
        print_image(grid, use_char=True, highlighter=partial(component_highlighter, components), margin=0)

    return price

def scan_edges(pts, dim0):
    dim1 = 1 - dim0
    line_d1s = sorted(set(p[dim1] for p in pts))
    prev_lefts, prev_rights = set(), set()
    edges = 0
    for d1v in line_d1s:
        line_d0s = sorted(p[dim0] for p in pts if p[dim1] == d1v)
        lefts = set(b for a, b in pairwise(line_d0s) if b - a != 1)
        rights = set(a for a, b in pairwise(line_d0s) if b - a != 1)
        lefts.add(line_d0s[0])
        rights.add(line_d0s[-1])
        edges += len(lefts - prev_lefts) + len(rights - prev_rights)
        prev_lefts, prev_rights = lefts, rights
    return edges

def part2(output=False):
    grid, inv = parse()
    ngh = {g: [a for a in pt.adj_ortho(g, grid) if a in inv[gv]] for g, gv in grid.items()}

    price = 0
    avail = set(grid)
    while avail:
        nodes = connected_component(ngh, avail.pop())
        area = len(nodes)
        perim = scan_edges(nodes, 0) + scan_edges(nodes, 1)
        price += area * perim
        avail.difference_update(nodes)

    return price

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
