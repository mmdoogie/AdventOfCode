from functools import partial
import re
from mrm.dijkstra import dijkstra, Dictlike

with open('data/aoc_2015/19.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    repls = []
    for d in dat:
        if '=>' in d:
            repls += [tuple(d.split(' => '))]
        elif d != '':
            base_molecule = d
    return repls, base_molecule

def fab_step(repls, base):
    results = set()
    for rs, rd in repls:
        rsi = re.finditer(rs, base)
        for s in rsi:
            chg = base[:s.start()] + rd + base[s.end():]
            results.add(chg)
    return results

def fab_step_rev(repls, base):
    results = set()
    for rs, rd in repls:
        rdi = re.finditer(rd, base)
        for d in rdi:
            chg = base[:d.start()] + rs + base[d.end():]
            results.add(chg)
    return results

def part1(output = True):
    repls, base = parse()
    r = fab_step(repls, base)
    return len(r)

def part2(output = True):
    repls, base = parse()
    d = Dictlike(partial(fab_step_rev, repls))
    w, p = dijkstra(d, start_point=base, end_point='e', keep_paths=True, dist_est=len)
    if output:
        for chg in p['e']:
            print(f'{len(chg):<3}', chg)
    return w['e']

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
