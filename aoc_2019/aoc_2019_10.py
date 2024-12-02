from math import gcd, atan2, pi
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def parse():
    with open('data/aoc_2019/10.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    asteroids = set()
    for y, l in enumerate(dat):
        for x, c in enumerate(l):
            if c == '#':
                asteroids.add(Point(x, y))
    return asteroids

def dist(src, dst):
    return abs(dst.x - src.x) + abs(dst.y - src.y)

def angle(slp):
    if slp.x < 0 and slp.y < 0:
        return atan2(slp.y, slp.x) + 5 * pi / 2
    else:
        return atan2(slp.y, slp.x) + pi / 2

def compute():
    asteroids = parse()
    visible = {}
    vslopes = {}
    for cand in asteroids:
        slopes = {}
        for oth in asteroids:
            if cand == oth:
                continue
            dx = oth.x - cand.x
            dy = oth.y - cand.y

            adx = abs(dx)
            ady = abs(dy)

            if adx == 0:
                dx = 0
                dy = dy // ady
            elif ady == 0:
                dx = dx // adx
                dy = 0
            elif adx == ady:
                dx = dx // adx
                dy = dy // ady
            else:
                dx = dx // gcd(adx, ady)
                dy = dy // gcd(adx, ady)

            slp = Point(dx, dy)
            dst = adx + ady
            if slp not in slopes:
                slopes[slp] = [oth]
            else: 
                slopes[slp] += [oth]

        visible[cand] = len(slopes.keys())
        vslopes[cand] = slopes

    return visible, vslopes

def part1(output=False):
    visible, _ = compute()
    _, max_visible = max(visible.items(), key = lambda x: x[1])
    return max_visible

def part2(output=False):
    visible, vslopes = compute()
    sta_loc, _ = max(visible.items(), key = lambda x: x[1])
    elim = sorted(vslopes[sta_loc].items(), key = lambda x: angle(x[0]))[199]
    dists = {x: dist(sta_loc, x) for x in elim[1]}
    last_ast = sorted(dists, key = lambda x: x[1])[0]
    return last_ast.x * 100 + last_ast.y

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
