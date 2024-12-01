from functools import partial
from itertools import pairwise

import mrm.ansi_term as ansi
from mrm.dijkstra import dijkstra, Dictlike
from mrm.point import adj_ortho, grid_as_dict
from mrm.tsp import held_karp

with open('data/aoc_2016/24.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def preprocess():
    nodes = grid_as_dict(dat, valid=lambda c: c in '.0123456789')
    pts = {int(v): k for k, v in sorted(nodes.items(), key = lambda x: x[1]) if v != '.'}

    sp_w = {}
    sp_p = {}
    for i, p in pts.items():
        w, p = dijkstra(Dictlike(partial(adj_ortho, constrain_pos=nodes)), start_point=p)
        for j, q in pts.items():
            sp_w[(i, j)] = w[q]
            sp_p[(i, j)] = p[q]

    return pts, sp_w, sp_p, nodes

def viz(grid, nodes, paths, min_path):
    path_pts = []
    for a, b in pairwise(min_path):
        path_pts += paths[(a, b)]
    for y in range(len(dat)):
        for x in range(len(dat[0])):
            pt = (x, y)
            if pt in nodes.values():
                print(ansi.red(str(list(nodes.values()).index(pt))), end='')
            elif pt in path_pts:
                print(ansi.green('*'), end='')
            elif pt in grid:
                print(' ', end='')
            else:
                print(ansi.cyan('#'), end='')
        print()

def part1(output = True):
    nodes, weights, paths, grid = preprocess()

    min_dist, min_path = held_karp(nodes, weights, dont_loop = True, start_point = 0)

    if output:
        ansi.clear_screen()
        print('Optimal path:', min_path)
        viz(grid, nodes, paths, min_path)

    return min_dist

def part2(output = True):
    nodes, weights, paths, grid = preprocess()

    min_dist, min_path = held_karp(nodes, weights)

    if output:
        ansi.clear_screen()
        print('Optimal path:', min_path)
        viz(grid, nodes, paths, min_path)

    return min_dist

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
