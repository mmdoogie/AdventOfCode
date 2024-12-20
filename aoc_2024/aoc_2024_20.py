from itertools import product

import mrm.cpoint as cpt
from mrm.dijkstra import Dictlike, dijkstra

def parse():
    with open('data/aoc_2024/20.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid, inv = cpt.grid_as_dict(lines, valid=lambda x: x in '.SE', with_inv=True)
    return grid, inv

def part1(output=False):
    grid, inv = parse()

    s_pt = list(inv['S'])[0]
    e_pt = list(inv['E'])[0]

    ngh = Dictlike(lambda x: cpt.adj_ortho(x, grid))
    from_s = dijkstra(ngh, start_point=s_pt, end_point=e_pt, keep_paths=False)
    to_e   = dijkstra(ngh, start_point=e_pt, keep_paths=False)
    bl_dist = from_s[e_pt]

    def cheats(s):
        return [s+2*h for h in cpt.HEADINGS if s+2*h in grid]

    good_cheats = 0
    for cheat_start in grid:
        for cheat_end in cheats(cheat_start):
            path_dist = from_s[cheat_start] + 2 + to_e[cheat_end]
            if bl_dist - path_dist >= 100:
                good_cheats += 1

    return good_cheats

def dist_grid(max_dist):
    grid = {}
    for x, y in product(range(-max_dist, max_dist + 1), repeat=2):
        pt = cpt.from_xy(x, y)
        dist = cpt.m_dist(pt)
        if dist > max_dist:
            continue
        grid[pt] = int(dist)
    return grid

def part2(output=False):
    grid, inv = parse()

    s_pt = list(inv['S'])[0]
    e_pt = list(inv['E'])[0]

    ngh = Dictlike(lambda x: cpt.adj_ortho(x, grid))
    from_s = dijkstra(ngh, start_point=s_pt, end_point=e_pt, keep_paths=False)
    to_e   = dijkstra(ngh, start_point=e_pt, keep_paths=False)
    bl_dist = from_s[e_pt]

    search_grid = dist_grid(20)
    def cheats(s):
        return {pt + s: dist for pt, dist in search_grid.items() if pt + s in grid}

    good_cheats = set()
    for cheat_start in grid:
        for cheat_end, cheat_len in cheats(cheat_start).items():
            if bl_dist - (from_s[cheat_start] + cheat_len + to_e[cheat_end]) >= 100:
                good_cheats.add((cheat_start, cheat_end))

    return len(good_cheats)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
