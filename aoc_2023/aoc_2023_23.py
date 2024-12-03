from collections import defaultdict

from mrm.dijkstra import dijkstra
from mrm.image import max_xy

with open('data/aoc_2023/23.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse(ignore_slopes = False):
    tiles = {}
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            if c == '#':
                continue
            if y == 0:
                start_pt = (x, y)
            if y == len(dat) - 1:
                end_pt = (x, y)

            if ignore_slopes:
                tiles[(x, y)] = '.'
            else:
                tiles[(x, y)] = c

    return tiles, start_pt, end_pt

def make_neigh(tiles):
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    nogo = {(-1, 0): '>', (0, -1): 'v', (0, 1): None, (1, 0): None}
    dest = {'>': (1, 0), 'v': (0, 1)}

    neigh = defaultdict(list)

    for t in tiles:
        tx, ty = t
        for fd in dirs:
            fdx, fdy = fd
            if (tx - fdx, ty - fdy) not in tiles and tx != 0 and ty != 0:
                continue
            if tiles[t] == '.':
                for td in dirs:
                    tdx, tdy = td
                    if (tdx != 0 and tdx == -fdx) or (tdy != 0 and tdy == -fdy):
                        continue
                    n = (tx + tdx, ty + tdy)
                    if n not in tiles or tiles[n] == nogo[td]:
                        continue
                    neigh[(t, fd)] += [(n, td)]
            else:
                td = dest[tiles[t]]
                tdx, tdy = td
                n = (tx + tdx, ty + tdy)
                if tiles[n] == nogo[td]:
                    continue
                neigh[(t, fd)] += [(n, td)]

    return neigh

def viz_path(tiles, path):
    max_x, max_y = max_xy(tiles)

    print('     ', end='')
    for x in range(max_x + 2):
        if x % 100 == 0:
            print(f'{x//100:<1d}', end='')
        else:
            print(' ', end='')
    print()
    print('     ', end='')
    for x in range(max_x + 2):
        if x % 10 == 0:
            print(f'{(x%100)//10:<1d}', end='')
        else:
            print(' ', end='')
    print()
    print('     ', end='')
    for x in range(max_x + 2):
        print(f'{x%10:<1d}', end='')
    print()
    for y in range(max_y + 1):
        print(f'{y:4d} ', end='')
        for x in range(max_x + 2):
            if (x, y) in path and tiles[(x, y)] == '.':
                print('*', end='')
            elif (x, y) in tiles:
                print(tiles[(x,y)], end='')
            else:
                print('#', end='')
        print()

def part1(output = True):
    tiles, start_pt, end_pt = parse()
    neigh = make_neigh(tiles)

    start = (start_pt, (0, 1))
    end = (end_pt, (0, 1))

    w, p = dijkstra(neigh, defaultdict(lambda: -1), start_point=start, danger_ignore_visited = True)

    if output:
        path = [p[0] for p in p[end]]
        viz_path(tiles, path)

    return -w[end]

def squash(neigh, adj, wts, vis, dp, from_pt, end_pt):
    n = neigh[from_pt]
    curr_dist = 0 if dp == from_pt else 1
    while len(n) == 1:
        curr_dist += 1
        from_pt = n[0]
        if from_pt[0] == end_pt[0]:
            break
        n = neigh[from_pt]
    if len(n) == 0:
        return
    adj[dp[0]].add(from_pt[0])
    adj[from_pt[0]].add(dp[0])
    wts[(dp[0], from_pt[0])] = curr_dist
    wts[(from_pt[0], dp[0])] = curr_dist
    if len(n) == 1:
        return
    for nextstart in n:
        if nextstart in vis:
            continue
        vis.add(nextstart)
        squash(neigh, adj, wts, vis, from_pt, nextstart, end_pt)
    return adj, wts

def explore(adj, wts, curr_dist, from_pt, end_pt, prev_dps):
    prev_dps.add(from_pt)
    neigh = adj[from_pt]

    max_dist = 0
    for n in neigh:
        if n in prev_dps:
            continue
        n_dist = curr_dist + wts[(from_pt, n)]
        if n == end_pt:
            return n_dist
        max_dist = max(max_dist, explore(adj, wts, n_dist, n, end_pt, set(prev_dps)))
    return max_dist

def part2(output = True):
    tiles, start_pt, end_pt = parse(ignore_slopes = True)
    neigh = make_neigh(tiles)

    start = (start_pt, (0, 1))
    end = (end_pt, (0, 1))

    adj, wts = squash(neigh, defaultdict(set), {}, set(), start, start, end)
    dist = explore(adj, wts, 0, start_pt, end_pt, set())

    return dist

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
