from mrm.dijkstra import dijkstra

def parse():
    with open('data/aoc_2019/06.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    pairs = [p.split(')') for p in dat]

    deps = {}
    objs = set()

    for a, b in pairs:
        objs.add(a)
        objs.add(b)

        if a in deps:
            deps[a] += [b]
        else:
            deps[a] = [b]

        if b in deps:
            deps[b] += [a]
        else:
            deps[b] = [a]

    return deps

def part1(output=False):
    deps = parse()
    com_weights, com_paths = dijkstra(deps, start_point='COM')
    return sum(com_weights.values())

def part2(output=False):
    deps = parse()
    you_weights, you_paths = dijkstra(deps, start_point='YOU')
    return you_weights['SAN'] - 2

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
