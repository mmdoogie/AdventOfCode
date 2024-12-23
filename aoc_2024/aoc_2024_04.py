from itertools import cycle

from mrm.ansi_term import green, red
from mrm.dijkstra import Dictlike
from mrm.image import print_image
from mrm.point import adj_diag, adj_ortho, grid_as_dict, point_add, point_sub

def parse():
    with open('data/aoc_2024/04.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return grid_as_dict(lines, with_inv=True)

def part1(output=False):
    grid, inv = parse()

    finds = set()
    cnt = 0
    for x_loc in inv['X']:
        for m_loc in adj_diag(x_loc, inv['M']):
            delta = point_sub(m_loc, x_loc)
            a_loc = point_add(m_loc, delta, 1)
            if a_loc not in inv['A']:
                continue
            s_loc = point_add(m_loc, delta, 2)
            if s_loc not in inv['S']:
                continue
            finds.update([x_loc, m_loc, a_loc, s_loc])
            cnt += 1

    if output:
        colors = cycle([green, red])
        def highlight(x, y, c):
            if (x, y) in finds:
                return next(colors)(c)
            return ' '
        print_image(grid, use_char=True, highlighter=highlight)

    return cnt

def part2(output=False):
    grid, inv = parse()

    finds = set()
    cnt = 0
    for a_loc in inv['A']:
        adj = sorted(set(adj_diag(a_loc, grid)) - set(adj_ortho(a_loc, grid)))
        corners = ''.join(grid[a] for a in adj)
        if corners in ['MMSS', 'MSMS', 'SSMM', 'SMSM']:
            cnt += 1
            finds.add(a_loc)
            finds.update(adj)

    if output:
        colors = cycle([green, red])
        def highlight(x, y, c):
            if (x, y) in finds:
                return next(colors)(c)
            return ' '
        print_image(grid, use_char=True, highlighter=highlight)

    return cnt

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
