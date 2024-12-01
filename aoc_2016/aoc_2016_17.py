from functools import partial
from hashlib import md5

from mrm.dijkstra import dijkstra, Dictlike

with open('data/aoc_2016/17.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    passcode = dat[0]
    lp = len(passcode)

gpv = {'D':1j,'U':-1j,'L':-1,'R':1}
def gridpoint(path):
    pt = sum(gpv[c] for c in path)
    return int(pt.real), int(pt.imag)

ncache = {}
def neighbors(curr, dontstoptil=0):
    if curr in ncache:
        return ncache[curr]
    path = curr[lp:]
    gpx, gpy = gridpoint(path)
    if gpx == 3 and gpy == 3:
        if len(path) > dontstoptil:
            return ['success']
        ncache[curr] = []
        return []
    h = md5(curr.encode('utf-8')).hexdigest()
    n = []
    for i, np in enumerate('UDLR'):
        if gpy == 0 and np == 'U':
            continue
        if gpy == 3 and np == 'D':
            continue
        if gpx == 0 and np == 'L':
            continue
        if gpx == 3 and np == 'R':
            continue
        if h[i] in 'bcdef':
            n += [curr + np]
    ncache[curr] = n
    return n

def part1(output = True):
    del output
    d = Dictlike(neighbors)
    _, p = dijkstra(d, start_point = passcode, end_point = 'success')
    return p['success'][-2][lp:]

def part2(output = True):
    longest = 0
    while True:
        d = Dictlike(partial(neighbors, dontstoptil=longest))
        w = dijkstra(d, start_point = passcode, end_point = 'success', keep_paths = False)
        if 'success' in w:
            longest = w['success'] - 1
            if output:
                print('Restarting, ignoring success at', longest)
        else:
            if output:
                print('No longer path found!')
            break

    return longest

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
