from functools import partial
from itertools import combinations

from mrm.dijkstra import dijkstra, Dictlike
from mrm.point import adj_ortho, m_dist

with open('data/aoc_2016/22.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    nodes = {}
    for d in dat:
        if not 'dev' in d:
            continue
        nn = tuple(int(v.strip('xy')) for v in d[:23].strip().split('-')[1:])
        us = int(d[29:35].strip()[:-1])
        av = int(d[35:41].strip()[:-1])
        nodes[nn] = (us, av)

def part1(output = True):
    viable = 0
    for a, b in combinations(nodes.values(), 2):
        if a[0] <= b[1] and a[0] != 0:
            viable += 1
            if output:
                print(f'{a[0]} from {a} fits into {b[1]} from {b}, {viable}')
        if b[0] <= a[1] and b[0] != 0:
            viable += 1
            if output:
                print(f'{b[0]} from {b} fits into {a[1]} from {a}, {viable}')

    return viable

def nfun(pt):
    neigh = adj_ortho(pt, nodes)
    for i in range(len(neigh)-1, -1, -1):
        if nodes[neigh[i]][0] > 200:
            del neigh[i]
    return neigh

def part2(output = True):
    sp = [k for k, v in nodes.items() if v[0] == 0][0]
    ep = (32, 1)
    w, p = dijkstra(Dictlike(nfun), start_point=sp, end_point=ep, dist_est=partial(m_dist, ep))

    if output:
        for y in range(31):
            for x in range(34):
                u, _ = nodes[(x, y)]
                if u == 0:
                    print('_', end='')
                elif u > 200:
                    print('#', end='')
                elif y == 0 and x == 33:
                    print('?', end='')
                elif y == 0 and x == 0:
                    print('x', end='')
                elif y == 0:
                    print('5', end='')
                elif x == 0 and y == 1:
                    print('2', end='')
                elif (x,  y) in p[ep]:
                    print('1', end='')
                else:
                    print('.', end='')
            print()

    return w[ep] + 5*32 + 2

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
