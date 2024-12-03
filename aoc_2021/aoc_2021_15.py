from mrm.dijkstra import dijkstra, Dictlike
from mrm.point import grid_as_dict, adj_ortho

with open('data/aoc_2021/15.txt') as f:
    dat = [[int(v) for v in list(x.strip())] for x in f.readlines()]

def part1(output=False):
    grid = grid_as_dict(dat)
    ngh = {g: adj_ortho(g, grid) for g in grid}
    def wt(st):
        _, d = st
        return grid[d]
    weights = dijkstra(ngh, Dictlike(wt), start_point=(0,0), end_point=(99,99), keep_paths=False)
    return weights[(99,99)]

def plusup(l, a):
    return [((v - 1 + a) % 9) + 1 for v in l]

def embiggenmap(dat):
    big = list()
    
    for y in range(5):
        for r in dat:
            big += [plusup(r, y+0) + plusup(r, y+1) + plusup(r, y+2) + plusup(r, y+3) + plusup(r, y+4)]
    
    return big

def part2(output=False):
    big = embiggenmap(dat)
    grid = grid_as_dict(big)
    ngh = {g: adj_ortho(g, grid) for g in grid}
    def wt(st):
        _, d = st
        return grid[d]
    weights = dijkstra(ngh, Dictlike(wt), start_point=(0,0), end_point=(499,499), keep_paths=False)
    return weights[(499,499)]
