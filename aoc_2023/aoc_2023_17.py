from collections import defaultdict

from mrm.dijkstra import dijkstra
from mrm.image import max_xy

with open('data/aoc_2023/17.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    grid = {}
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            grid[(x, y)] = int(c)
    return grid

LEFT   = (-1,  0)
RIGHT  = ( 1,  0)
UP     = ( 0, -1)
DOWN   = ( 0,  1)
NONE   = ( 0,  0)
ORTHOG = {LEFT:  [UP,   DOWN],
          RIGHT: [UP,   DOWN],
          UP:    [LEFT, RIGHT],
          DOWN:  [LEFT, RIGHT],
          NONE:  [LEFT, RIGHT, UP, DOWN]}

def build_adj(grid, min_moves = 1, max_moves = 3):
    adj = defaultdict(set)
    wts = {}
    for g in grid:
        gx, gy = g
        for from_dir in ORTHOG[NONE] if g != (0, 0) else [NONE]:
            for to_dir in ORTHOG[from_dir]:
                wt = 0
                for step in range(1, max_moves + 1):
                    dx, dy = gx + step * to_dir[0], gy + step * to_dir[1]
                    if (dx, dy) not in grid:
                        break
                    wt += grid[(dx, dy)]
                    if step >= min_moves:
                        adj[(gx, gy, from_dir)].add((dx, dy, to_dir))
                        wts[((gx, gy, from_dir), (dx, dy, to_dir))] = wt
    return adj, wts

def part1(output = True):
    grid = parse()
    max_x, max_y = max_xy(grid)
    adj, wts = build_adj(grid)

    if output:
        print(f'Grid size: {max_x + 1} x {max_y + 1} ({len(grid)} cells)')
        print(f'Adj graph: {len(wts)} edges')

    start = (0, 0, NONE)
    ends = [(max_x, max_y, DOWN), (max_x, max_y, RIGHT)]
    weights = dijkstra(adj, wts, start_point = start, end_point = ends, keep_paths = False)

    sol_weights = [weights[e] for e in ends]
    if output:
        print('Solution weights:', sol_weights)

    return min(sol_weights)

def part2(output = True):
    grid = parse()
    max_x, max_y = max_xy(grid)
    adj, wts = build_adj(grid, 4, 10)

    if output:
        print(f'Grid size: {max_x + 1} x {max_y + 1} ({len(grid)} cells)')
        print(f'Adj graph: {len(wts)} edges')

    start = (0, 0, NONE)
    ends = [(max_x, max_y, DOWN), (max_x, max_y, RIGHT)]
    weights = dijkstra(adj, wts, start_point = start, end_point = ends, keep_paths = False)

    sol_weights = [weights[e] for e in ends]
    if output:
        print('Solution weights:', sol_weights)

    return min(sol_weights)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
