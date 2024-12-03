from itertools import combinations

from mrm.point import m_dist

with open('data/aoc_2023/11.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse(empty_extra = 1):
    galaxies = set()
    empty_x = [True] * len(dat[0])
    empty_y = []
    for y, d in enumerate(dat):
        if all(c == '.' for c in d):
            empty_y += [y]
            continue
        for x, c in enumerate(d):
            if c == '#':
                galaxies.add((x, y))
                empty_x[x] = False
    empty_x = [i for i, x in enumerate(empty_x) if x]

    new_galaxies = set()
    for g in galaxies:
        add_x = empty_extra * sum(g[0] > x for x in empty_x)
        add_y = empty_extra * sum(g[1] > y for y in empty_y)
        new_galaxies.add((g[0] + add_x, g[1] + add_y))

    return new_galaxies

def part1(output = True):
    galaxies = parse(empty_extra = 1)

    pair_dist = [m_dist(a, b) for a, b in combinations(galaxies, 2)]
    if output:
        print('Galaxy count:', len(galaxies))
        print('Combinations:', len(pair_dist))
        print('Min  dist:   ', min(pair_dist))
        print('Max  dist:   ', max(pair_dist))
        print('Mean dist:   ', sum(pair_dist) // len(pair_dist))

    return sum(pair_dist)

def part2(output = True):
    galaxies = parse(empty_extra = 1000000 - 1)

    pair_dist = [m_dist(a, b) for a, b in combinations(galaxies, 2)]
    if output:
        print('Min  dist:   ', min(pair_dist))
        print('Max  dist:   ', max(pair_dist))
        print('Mean dist:   ', sum(pair_dist) // len(pair_dist))

    return sum(pair_dist)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
