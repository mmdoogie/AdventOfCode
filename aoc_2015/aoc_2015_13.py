from itertools import pairwise

from mrm.tsp import held_karp

with open('data/aoc_2015/13.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def make_graph():
    pts = set()
    wts = {}
    for d in dat:
        p = d.split(' ')
        n1 = p[0]
        n2 = p[10].strip('.')
        sgn = -1 if p[2] == 'lose' else 1
        units = int(p[3])
        weight = sgn * units

        pts.add(n1)
        pts.add(n2)
        if (n2, n1) in wts:
            weight += wts[(n2, n1)]
            wts[(n2, n1)] = weight
        wts[(n1, n2)] = weight

    return pts, wts

def part1(output = True):
    pts, wts = make_graph()
    w, p = held_karp(pts, wts, min_fn = max)

    if output:
        print('Optimal Order:', p)
        for pa, pb in pairwise(p):
            print(pa, 'beside', pb, 'contributes', wts[(pa, pb)])

    return w

def part2(output = True):
    pts, wts = make_graph()
    for p in pts:
        wts[(p, 'Doogie')] = 0
        wts[('Doogie', p)] = 0
    pts.add('Doogie')
    w, p = held_karp(pts, wts, min_fn = max)

    if output:
        print('Optimal Order:', p)
        for pa, pb in pairwise(p):
            print(pa, 'beside', pb, 'contributes', wts[(pa, pb)])

    return w

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
