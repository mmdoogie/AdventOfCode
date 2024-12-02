from collections import deque
from mrm.dijkstra import dijkstra

def map_region(part2 = None):
    with open('data/aoc_2019/18.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    spaces = {}
    doors = {}
    keys = {}
    for y, line in enumerate(dat):
        for x, c in enumerate(line):
            if c == '#':
                continue
            spaces[(x, y)] = True
            if c == '@':
                start_pos = (x, y)
            if c in 'abcdefghijklmnopqrstuvwxyz':
                keys[c] = (x, y)
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                doors[c] = (x, y)

    if part2 is not None:
        sx, sy = start_pos
        del spaces[(sx, sy)]
        del spaces[(sx - 1, sy)]
        del spaces[(sx + 1, sy)]
        del spaces[(sx, sy - 1)]
        del spaces[(sx, sy + 1)]
        dx, dy = part2
        start_pos = (sx + dx, sx + dy)

    neighbors = {}
    for sx, sy in spaces.keys():
        adj = [(sx - 1, sy), (sx + 1, sy), (sx, sy - 1), (sx, sy + 1)]
        sn = [a for a in adj if a in spaces]
        neighbors[(sx, sy)] = sn

    pathfind = {}
    pathfind['@'] = dijkstra(neighbors, start_point=start_pos)
    for kk, kv in keys.items():
        pathfind[kk] = dijkstra(neighbors, start_point=kv)

    pair_dist = {}
    for k1 in list(keys.keys()) + ['@']:
        dists = {}
        for k2 in keys.keys():
            if k1 == k2:
                continue
            try:
                dists[k2] = pathfind[k1][0][keys[k2]]
            except:
                pass
        pair_dist[k1] = dists

    blockers = {}
    for k in keys.keys():
        kblk = []
        for dk, dv in doors.items():
            try:
                if dv in pathfind['@'][1][keys[k]]:
                    kblk += [str.lower(dk)]
            except:
                pass
        blockers[k] = kblk

    return pair_dist, blockers

def valid_moves(pair_dist, blockers, pos, have_keys):
    return [have_keys + ':' + pos + ':' + k for k in pair_dist[pos].keys() if k not in have_keys and all([b in have_keys for b in blockers[k]])]

def part1(output=False):
    pair_dist, blockers = map_region()
    explored = {}
    paths = valid_moves(pair_dist, blockers, '@', '')

    while True:
        new_paths = set()
        for p in paths:
            hk, cp, np = p.split(':')

            ek = hk + ':' + cp
            try:
                cw = explored[ek]
            except:
                cw = 0

            cw += pair_dist[cp][np]

            nhk = ''.join(sorted(hk + np))
            ek = nhk + ':' + np
            if (ek in explored and cw < explored[ek]) or ek not in explored:
                explored[ek] = cw

            new_paths.update(valid_moves(pair_dist, blockers, np, nhk))
        paths = new_paths
        if len(new_paths) == 0:
            break

    full_sets = [k for k in explored.keys() if len(k) == 28]
    scores = [explored[p] for p in full_sets]

    return min(scores)

def valid_moves_4up(pair_dist, blockers, pos, have_keys):
    moves = []
    for i in range(4):
        moves += [have_keys + ':' + pos + ':' + str(i) + ':' + k for k in pair_dist[i][pos[i]].keys() if k not in have_keys and all([b in have_keys for b in blockers[i][k]])]
    return moves

def part2(output=False):
    offsets = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    pair_dist = {}
    blockers = {}
    for i, o in enumerate(offsets):
        pair_dist[i], blockers[i] = map_region(part2 = o)

    explored = {}
    paths = valid_moves_4up(pair_dist, blockers, '@@@@', '')

    while True:
        new_paths = set()
        for p in paths:
            hk, cp, ss, np = p.split(':')
            ss = int(ss)

            ek = hk + ':' + cp
            try:
                cw = explored[ek]
            except:
                cw = 0

            cw += pair_dist[ss][cp[ss]][np]

            nhk = ''.join(sorted(hk + np))
            nnp = cp[0:ss] + np + cp[ss+1:4]
            ek = nhk + ':' + nnp
            if (ek in explored and cw < explored[ek]) or ek not in explored:
                explored[ek] = cw

            new_paths.update(valid_moves_4up(pair_dist, blockers, nnp, nhk))
        paths = new_paths
        if len(new_paths) == 0:
            break

    full_sets = [k for k in explored.keys() if len(k) == 31]
    scores = [explored[p] for p in full_sets]

    return min(scores)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
