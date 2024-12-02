from mrm.dijkstra import dijkstra

def parse_map():
    with open('data/aoc_2019/20.txt') as f:
        dat = [x.strip('\n') for x in f.readlines()]

    spaces = {}
    portals = {}
    partial_portals = {}
    for y, line in enumerate(dat):
        for x, c in enumerate(line):
            match c:
                case '#' | ' ':
                    continue
                case '.':
                    spaces[(x, y)] = True
                    continue
                case _:
                    if (x, y-1) in partial_portals:
                        first_letter = partial_portals[(x, y-1)]
                        portal_name = first_letter + c
                        if portal_name in portals:
                            if (x, y-2) in spaces:
                                portals[portal_name] += [(x, y-2)]
                            else:
                                portals[portal_name] += [(x, y+1)]
                        else:
                            if (x, y-2) in spaces:
                                portals[portal_name] = [(x, y-2)]
                            else:
                                portals[portal_name] = [(x, y+1)]
                        del partial_portals[(x, y-1)]
                    elif (x-1, y) in partial_portals:
                        first_letter = partial_portals[(x-1, y)]
                        portal_name = first_letter + c
                        if portal_name in portals:
                            if (x-2, y) in spaces:
                                portals[portal_name] += [(x-2, y)]
                            else:
                                portals[portal_name] += [(x+1, y)]
                        else:
                            if (x-2, y) in spaces:
                                portals[portal_name] = [(x-2, y)]
                            else:
                                portals[portal_name] = [(x+1, y)]
                        del partial_portals[(x-1, y)]
                    else:
                        partial_portals[(x, y)] = c

    return spaces, portals

def make_neighbors(spaces, portals):
    neighbors = {}
    for sx, sy in spaces.keys():
        adj_pts = [(sx-1, sy), (sx+1, sy), (sx, sy-1), (sx, sy+1)]
        ngh = [a for a in adj_pts if a in spaces]
        neighbors[(sx, sy)] = ngh

    for p in portals.values():
        if len(p) == 1:
            continue
        p1, p2 = p
        if p1 in neighbors:
            neighbors[p1] += [p2]
        else:
            neighbors[p1] = [p2]
        if p2 in neighbors:
            neighbors[p2] += [p1]
        else:
            neighbors[p2] = [p1]

    return neighbors

def part1(output=False):
    spaces, portals = parse_map()
    neighbors = make_neighbors(spaces, portals)

    aa_pt = portals['AA'][0]
    zz_pt = portals['ZZ'][0]

    weights = dijkstra(neighbors, start_point=aa_pt, end_point=zz_pt, keep_paths=False)

    return weights[zz_pt]

def split_portals(portals):
    inner_portals = {}
    outer_portals = {}

    for pn, pp in portals.items():
        if pn == 'AA' or pn == 'ZZ':
            continue
        if pp[0][0] == 2 or pp[0][0] == 122 or pp[0][1] == 2 or pp[0][1] == 118:
            outer_portals[pn] = pp
            inner_portals[pn] = [pp[1], pp[0]]
        if pp[1][0] == 2 or pp[1][0] == 122 or pp[1][1] == 2 or pp[1][1] == 118:
            outer_portals[pn] = [pp[1], pp[0]]
            inner_portals[pn] = pp

    return inner_portals, outer_portals

def part2(output=False):
    spaces, portals = parse_map()
    inner_portals, outer_portals = split_portals(portals)
    neighbors = make_neighbors(spaces, {})

    full_neighbors = {}
    full_weights = {}

    aa = ('AA', 'out', 0)
    zz = ('ZZ', 'out', 0)

    weights = dijkstra(neighbors, start_point=portals['AA'][0], keep_paths=False)
    for p in inner_portals.keys():
        if inner_portals[p][0] in weights:
            pp = (p, 'in', 0)
            if aa in full_neighbors:
                full_neighbors[aa] += [pp]
            else:
                full_neighbors[aa] = [pp]
            full_weights[(aa, pp)] = weights[inner_portals[p][0]]

    weights = dijkstra(neighbors, start_point=portals['ZZ'][0], keep_paths=False)
    for p in inner_portals.keys():
        if inner_portals[p][0] in weights:
            pp = (p, 'in', 0)
            if pp in full_neighbors:
                full_neighbors[pp] += [zz]
            else:
                full_neighbors[pp] = [zz]
            full_weights[(pp, zz)] = weights[inner_portals[p][0]]

    max_depth = 30
    for d in range(0, max_depth):
        for op in outer_portals.keys():
            weights = dijkstra(neighbors, start_point=outer_portals[op][0], keep_paths=False)
            nn = []
            oo = (op, 'out', d)
            for op2 in outer_portals.keys():
                if op == op2:
                    continue
                oo2 = (op2, 'out', d)
                if outer_portals[op2][0] in weights:
                    nn += [oo2]
                    full_weights[(oo, oo2)] = weights[outer_portals[op2][0]]
            for ip in inner_portals.keys():
                if inner_portals[ip][0] in weights:
                    ii = (ip, 'in', d)
                    nn += [ii]
                    full_weights[(oo, ii)] = weights[inner_portals[ip][0]]
            if len(nn) > 0 and oo in full_neighbors:
                full_neighbors[oo] += nn
            else:
                full_neighbors[oo] = nn

        for ip in inner_portals.keys():
            weights = dijkstra(neighbors, start_point=inner_portals[ip][0], keep_paths=False)
            nn = []
            ii = (ip, 'in', d)
            for ip2 in inner_portals.keys():
                if ip == ip2:
                    continue
                ii2 = (ip2, 'in', d)
                if inner_portals[ip2][0] in weights:
                    nn += [ii2]
                    full_weights[(ii, ii2)] = weights[inner_portals[ip2][0]]
            for op in outer_portals.keys():
                if outer_portals[op][0] in weights:
                    oo = (op, 'out', d)
                    nn += [oo]
                    full_weights[(ii, oo)] = weights[outer_portals[op][0]]
            if len(nn) > 0 and ii in full_neighbors:
                full_neighbors[ii] += nn
            else:
                full_neighbors[ii] = nn

        if d > 0:
            for op in outer_portals.keys():
                oo = (op, 'out', d)
                ii = (op, 'in', d-1)
                full_neighbors[oo] += [ii]
                full_weights[(oo, ii)] = 1

        if d < max_depth - 1:
            for ip in inner_portals.keys():
                ii = (ip, 'in', d)
                oo = (ip, 'out', d+1)
                full_neighbors[ii] += [oo]
                full_weights[(ii, oo)] = 1

    weights = dijkstra(full_neighbors, full_weights, start_point=aa, end_point=zz, keep_paths=False)
    return weights[zz]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
