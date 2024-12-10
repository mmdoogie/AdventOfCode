from mrm.dijkstra import dijkstra
import mrm.point as pt

def parse():
    with open('data/aoc_2024/10.txt', 'r', encoding='utf8') as f:
        lines = [[int(c) for c in l.strip('\n')] for l in f.readlines()]
    grid, inv = pt.grid_as_dict(lines, valid=lambda x: x != '.', with_inv=True)
    ngh = {g: [a for a in pt.adj_ortho(g, grid) if grid[a] - grid[g] == 1] for g in grid}
    return inv, ngh

def part1(output=False):
    inv, ngh = parse()
    starts = inv[0]
    ends = list(inv[9])

    score = 0
    for s in starts:
        w = dijkstra(ngh, start_point=s, end_point=ends, keep_paths=False)
        score += sum(e in w for e in ends)
    return score

def bfs(ngh, start):
    paths = [[start]]
    explored = True
    while explored:
        explored = False
        to_add = []
        for p in paths:
            adj = ngh[p[-1]]
            if not adj:
                continue
            for a in adj[1:]:
                to_add += [p + [a]]
            p += [adj[0]]
            explored = True
        paths += to_add
    return paths

def part2(output=False):
    inv, ngh = parse()
    starts = inv[0]
    score = sum(sum(len(b) == 10 for b in bfs(ngh, s)) for s in starts)
    return score

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
