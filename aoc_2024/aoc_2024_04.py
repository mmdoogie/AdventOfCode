from itertools import cycle

from mrm.ansi_term import green, red
from mrm.dijkstra import Dictlike
from mrm.image import print_image
from mrm.point import adj_diag, adj_ortho, grid_as_dict, point_add, point_sub

def parse():
    with open('data/aoc_2024/04.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return grid_as_dict(lines)


def part1(output=False):
    grid = parse()
    starts = [pt for pt, ch in grid.items() if ch == 'X']

    m_filter = Dictlike(lambda: 0, lambda x: x in grid and grid[x] == 'M')

    finds = set()
    cnt = 0
    for x_loc in starts:
        for m_loc in adj_diag(x_loc, m_filter):
            delta = point_sub(m_loc, x_loc)
            a_loc = point_add(m_loc, delta, 1)
            if a_loc not in grid or grid[a_loc] != 'A':
                continue
            s_loc = point_add(m_loc, delta, 2)
            if s_loc not in grid or grid[s_loc] != 'S':
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
    grid = parse()
    starts = [pt for pt, ch in grid.items() if ch == 'A']

    finds = set()
    cnt = 0
    for a_loc in starts:
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
