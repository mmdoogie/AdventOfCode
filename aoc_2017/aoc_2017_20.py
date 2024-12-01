from collections import defaultdict
from itertools import combinations
import re

import mrm.point as pt

with open('data/aoc_2017/20.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    pva_re = re.compile('p=<([0-9,-]+)>, v=<([0-9,-]+)>, a=<([0-9,-]+)>')

def pos(p, v, a, t):
    # pain point!
    # 1/2*a*t^2 from continuous physics
    # here, with discrete steps we are adding sum(1..t)=t*(t+1)/2
    afact = 0.5 * t * (t + 1)
    return [p[0] + v[0] * t + a[0] * afact,
            p[1] + v[1] * t + a[1] * afact,
            p[2] + v[2] * t + a[2] * afact]

def crash(p1, v1, a1, p2, v2, a2):
    aa = a1[0]/2 - a2[0]/2
    if aa == 0:
        return None
    bb = v1[0] + a1[0]/2 - v2[0] - a2[0]/2
    cc = p1[0] - p2[0]

    t1 = (-bb + pow(bb * bb - 4 * aa * cc, 0.5)) / (2 * aa)
    t2 = (-bb - pow(bb * bb - 4 * aa * cc, 0.5)) / (2 * aa)

    if not isinstance(t1, complex) and t1 >= 0:
        pos1 = pos(p1, v1, a1, t1)
        pos2 = pos(p2, v2, a2, t1)
        if pt.m_dist(pos1, pos2) < 0.5:
            return t1
    if not isinstance(t2, complex) and t2 >= 0:
        pos1 = pos(p1, v1, a1, t2)
        pos2 = pos(p2, v2, a2, t2)
        if pt.m_dist(pos1, pos2) < 0.5:
            return t2

    return None

def part1(output = True):
    pva = [[[int(v) for v in l.split(',')] for l in pva_re.match(d).groups()] for d in dat]

    t = 1
    ts = 2
    prev_particles = []
    while True:
        dists = [pt.m_dist(pt.ZERO_3D, pos(p, v, a, t)) for p, v, a in pva]
        min_dist = min(dists)
        particle = dists.index(min_dist)
        if output:
            print('Particle', particle, 'min at dist', min_dist, 'at timestep', t)
        if len(prev_particles) > 20 and all(p == particle for p in prev_particles[-10:]):
            return particle
        prev_particles += [particle]
        t *= ts

    return 0

def part2(output = True):
    pva = {i: [[int(v) for v in l.split(',')] for l in pva_re.match(d).groups()] for i, d in enumerate(dat)}
    hits = defaultdict(list)
    for p1, p2 in combinations(pva.keys(), 2):
        tt = crash(*pva[p1], *pva[p2])
        if tt is not None:
            hits[tt] += [(p1, p2)]
    remain = set(pva.keys())
    for tt in sorted(hits.keys()):
        remove = set()
        for p1, p2 in hits[tt]:
            if p1 in remain and p2 in remain:
                remove.add(p1)
                remove.add(p2)
        remain -= remove
        if output:
            print(f'Timestep: {int(tt):3}, Removed: {len(remove):3}, Remain: {len(remain):3}')

    return len(remain)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
