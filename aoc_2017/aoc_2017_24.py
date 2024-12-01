with open('data/aoc_2017/24.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    compos = [tuple(int(x) for x in d.split('/')) for d in dat]
    all_ports = set(c[0] for c in compos).union(set(c[1] for c in compos))
    reachable = {p: {i for i, c in enumerate(compos) if p in c} for p in all_ports}

def explore(from_node, from_side, from_weight, from_used, metric):
    curr_node = compos[from_node]
    from_weight += curr_node[from_side]

    curr_side = 1 - from_side
    side_value = curr_node[curr_side]
    from_weight += side_value

    from_used.add(from_node)
    remain = reachable[side_value].difference(from_used)

    if len(remain) == 0:
        return metric(from_weight, from_used), from_weight, from_used

    res = [explore(r, compos[r].index(curr_node[curr_side]), from_weight, set(from_used), metric) for r in remain]
    return max(res)

def part1(output = True):
    start_nodes = [i for i, c in enumerate(compos) if 0 in c]
    if output:
        print('Valid Starting Nodes: ', start_nodes, [compos[s] for s in start_nodes])

    ex = [explore(s, compos[s].index(0), 0, set(), lambda w, u: w) for s in start_nodes]
    return max(ex)[0]

def part2(output = True):
    del output

    start_nodes = [i for i, c in enumerate(compos) if 0 in c]

    ex = [explore(s, compos[s].index(0), 0, set(), lambda w, u: len(u)) for s in start_nodes]
    return max(ex)[1]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
