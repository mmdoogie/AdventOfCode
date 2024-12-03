from collections import defaultdict

import mrm.ansi_term as ansi
from mrm.image import min_xy, max_xy

with open('data/aoc_2023/16.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    tiles = {}
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            tiles[(x, y)] = c

    return tiles

def visualize(tiles, visited):
    min_x, min_y = min_xy(tiles)
    max_x, max_y = max_xy(tiles)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in visited:
                print(ansi.green('#'), end = '')
            else:
                print(tiles[(x, y)], end = '')
        print()

RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)
UP = (0, -1)

SPLIT_Y = [(0, 1), (0, -1)]
SPLIT_X = [(1, 0), (-1, 0)]

NEXT_DIR = {(RIGHT, '\\'): DOWN,
            (RIGHT,  '/'): UP,
            (RIGHT,  '-'): RIGHT,
            (RIGHT,  '|'): SPLIT_Y,
            (LEFT,  '\\'): UP,
            (LEFT,   '/'): DOWN,
            (LEFT,   '-'): LEFT,
            (LEFT,   '|'): SPLIT_Y,
            (DOWN,  '\\'): RIGHT,
            (DOWN,   '/'): LEFT,
            (DOWN,   '-'): SPLIT_X,
            (DOWN,   '|'): DOWN,
            (UP,    '\\'): LEFT,
            (UP,     '/'): RIGHT,
            (UP,     '-'): SPLIT_X,
            (UP,     '|'): UP}

def traverse(tiles, visited, loc, initial_dir):
    x, y = loc
    curr_dir = initial_dir

    while (x, y) in tiles and curr_dir not in visited[(x, y)]:
        visited[(x, y)].add(curr_dir)
        tile = tiles[(x, y)]
        if tile != '.':
            curr_dir = NEXT_DIR[(curr_dir, tile)]
            if isinstance(curr_dir, list):
                for d in curr_dir:
                    traverse(tiles, visited, (x + d[0], y + d[1]), d)
                break
        x, y = x + curr_dir[0], y + curr_dir[1]

def part1(output = True):
    tiles = parse()
    visited = defaultdict(set)
    traverse(tiles, visited, (0, 0), RIGHT)
    if output:
        visualize(tiles, visited)

    return len(visited)

def part2(output = True):
    tiles = parse()
    max_x, max_y = max_xy(tiles)

    max_visited = 0
    saved_visited = None

    for x in range(max_x + 1):
        visited = defaultdict(set)
        traverse(tiles, visited, (x, 0), DOWN)
        if (l := len(visited)) >= max_visited:
            max_visited = l
            saved_visited = visited
            if output:
                print(f'({x:3d}, {0:3d}), DOWN : {l}')

        visited = defaultdict(set)
        traverse(tiles, visited, (x, max_y), UP)
        if (l := len(visited)) >= max_visited:
            max_visited = l
            saved_visited = visited
            if output:
                print(f'({x:3d}, {max_y:3d}), UP   : {l}')

    for y in range(max_y + 1):
        visited = defaultdict(set)
        traverse(tiles, visited, (0, y), RIGHT)
        if (l := len(visited)) >= max_visited:
            max_visited = l
            saved_visited = visited
            if output:
                print(f'({0:3d}, {y:3d}), RIGHT: {l}')

        visited = defaultdict(set)
        traverse(tiles, visited, (max_x, y), LEFT)
        if (l := len(visited)) >= max_visited:
            max_visited = l
            saved_visited = visited
            if output:
                print(f'({max_x:3d}, {y:3d}), LEFT : {l}')

    if output:
        visualize(tiles, saved_visited)

    return max_visited

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
