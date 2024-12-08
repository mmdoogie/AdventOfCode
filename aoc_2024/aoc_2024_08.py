from itertools import combinations
import string

import mrm.cpoint as cpt

def parse():
    with open('data/aoc_2024/08.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return cpt.grid_as_dict(lines, with_inv = True)

VALID_FREQ = string.ascii_letters + string.digits

def part1(output=False):
    grid, inv = parse()

    antinodes = set()
    for freq, locs in inv.items():
        if freq not in VALID_FREQ:
            continue
        for loc_a, loc_b in combinations(locs, 2):
            diff = loc_b - loc_a
            node = loc_a - diff
            if node in grid:
                antinodes.add(node)
            node = loc_b + diff
            if node in grid:
                antinodes.add(node)

    return len(antinodes)

def part2(output=False):
    grid, inv = parse()

    antinodes = set()
    for freq, locs in inv.items():
        if freq not in VALID_FREQ:
            continue
        for loc_a, loc_b in combinations(locs, 2):
            diff = loc_b - loc_a
            node = loc_a
            while node in grid:
                antinodes.add(node)
                node -= diff
            node = loc_b
            while node in grid:
                antinodes.add(node)
                node += diff

    return len(antinodes)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
