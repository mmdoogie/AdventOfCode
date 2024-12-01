from mrm.dijkstra import dijkstra

with open('data/aoc_2017/12.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    conns = {}
    for d in dat:
        node, pipes = d.split(' <-> ', 2)
        conns[int(node)] = [int(x) for x in pipes.split(', ')]

def part1(output = True):
    weights, paths = dijkstra(conns, start_point = 0)

    if output:
        print('Nodes in Group 0')
        for n in weights:
            print(f'Node {n:4} reachable wt {weights[n]} via {paths[n]}')

    return len(weights)

def part2(output = True):
    nodes = set(conns.keys())
    singular = {n for n, p in conns.items() if len(p) == 1 and p[0] == n}
    groups = len(singular)
    nodes -= singular

    if output:
        print(f'{groups} singular groups: {singular}')

    while nodes:
        group_node = nodes.pop()
        weights = dijkstra(conns, start_point = group_node, keep_paths = False)
        reachable = set(weights.keys())
        nodes -= reachable
        groups += 1
        if output:
            print(f'Group {groups} from {group_node} hits {reachable}')

    return groups

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
