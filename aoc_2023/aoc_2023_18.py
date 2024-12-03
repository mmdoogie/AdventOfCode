from collections import deque
from itertools import pairwise

from mrm.image import print_image
from mrm.point import adj_ortho, polygon_grid_squares

with open('data/aoc_2023/18.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1_alt_floodfill(output = True):
    loop = {}
    x, y = 0, 0
    for d in dat:
        dig_dir, dig_dist, _ = d.split(' ')
        for _ in range(int(dig_dist)):
            match dig_dir:
                case 'U':
                    y -= 1
                case 'D':
                    y += 1
                case 'L':
                    x -= 1
                case 'R':
                    x += 1
            loop[(x, y)] = '*'

    loop[(0,0)] = 'S'

    inside = {}
    inside[(1,0)] = True
    explore = deque([(1, 0)])
    while len(explore) > 0:
        if output:
            print(len(explore))
        pt = explore.pop()
        for a in adj_ortho(pt):
            if a in loop or a in inside:
                continue
            inside[a] = '+'
            explore.append(a)

    for l in loop:
        inside[l] = '*'
    inside[(0, 0)] = 'S'

    if output:
        print_image(inside, use_char = True)

    return len(inside)

def parse_crossings(for_part2 = False):
    loop_vert = []
    loop_horiz = {}

    x, y = 0, 0
    for d in dat:
        if for_part2:
            _, _, colorcode = d.split(' ')
            hexval = colorcode.split('#')[1].split(')')[0]
            dig_dist = int(hexval[:5], 16)
            dig_dir = hexval[5]
        else:
            dig_dir, dig_dist, _ = d.split(' ')
        start_x, start_y = x, y
        match dig_dir:
            case 'U' | '3':
                y -= int(dig_dist)
                loop_vert += [(y, start_y, x, dig_dir)]
            case 'D' | '1':
                y += int(dig_dist)
                loop_vert += [(start_y, y, x, dig_dir)]
            case 'L' | '2':
                x -= int(dig_dist)
                loop_horiz[(start_x, y)] = x
                loop_horiz[(x, y)] = start_x
            case 'R' | '0':
                x += int(dig_dist)
                loop_horiz[(start_x, y)] = x
                loop_horiz[(x, y)] = start_x

    loop_vert.sort()

    return loop_horiz, loop_vert

def crossings_for_row(loop_horiz, loop_vert, y):
    all_cross = []
    for sy, ey, x, dd in loop_vert:
        if sy <= y <= ey:
            all_cross += [(x, dd)]
        if sy > y:
            break
    all_cross.sort()

    toggle_cross = []
    curr_dir = None
    for x, dd in all_cross:
        if dd != curr_dir:
            toggle_cross += [x]
            curr_dir = dd
        elif dd in ['D', '1']:
            toggle_cross[-1] = x

    merge = []
    ltc = len(toggle_cross)
    for i in range(ltc // 2):
        if 2 * i + 2 >= ltc:
            break
        x1 = toggle_cross[2 * i + 1]
        x2 = toggle_cross[2 * i + 2]
        if (x1, y) in loop_horiz and loop_horiz[(x1, y)] == x2:
            merge += [x1, x2]

    return [x for x in toggle_cross if x not in merge]

def compute_area(loop_horiz, loop_vert, output = False):
    area = 0
    key_y = sorted({item for v in loop_vert for item in [v[0], v[0] + 1, v[1], v[1] + 1]})

    for y, next_y in pairwise(key_y):
        cfr = crossings_for_row(loop_horiz, loop_vert, y)
        rows = next_y - y
        for i in range(len(cfr) // 2):
            area += rows * (cfr[2 * i + 1] - cfr[2 * i] + 1)
            if output:
                print(y, rows, area)
    return area

def part1(output = True):
    loop_horiz, loop_vert = parse_crossings(for_part2 = False)

    area = compute_area(loop_horiz, loop_vert, output)

    if output:
        min_y = min(v[0] for v in loop_vert)
        max_y = max(v[1] for v in loop_vert)
        ic = {}
        for y in range(min_y, max_y + 1):
            cfr = crossings_for_row(loop_horiz, loop_vert, y)
            for i in range(len(cfr) // 2):
                for x in range(cfr[2 * i] + 1, cfr[2 * i + 1]):
                    ic[(x, y)] = '#'
                ic[(cfr[2 * i], y)] = '|'
                ic[(cfr[2 * i + 1], y)] = '|'
        for k, v in loop_horiz.items():
            for x in range(k[0], v + 1):
                y = k[1]
                if (x, y) in ic:
                    ic[(x, y)] = '='
                else:
                    ic[(x, y)] = '-'

        print_image(ic, use_char=True)

    return area

def part2(output = True):
    loop_horiz, loop_vert = parse_crossings(for_part2 = True)

    min_y = min(v[0] for v in loop_vert)
    min_x = min(v[2] for v in loop_vert)
    max_y = max(v[1] for v in loop_vert)
    max_x = max(v[2] for v in loop_vert)

    if output:
        print('X Range:', min_x, 'to', max_x)
        print('Y Range:', min_y, 'to', max_y)

    area = compute_area(loop_horiz, loop_vert, output)

    return area

def parse_pts(for_part2 = False):
    pts = [(0, 0)]

    x, y = 0, 0
    for d in dat:
        if for_part2:
            _, _, colorcode = d.split(' ')
            hexval = colorcode.split('#')[1].split(')')[0]
            dig_dist = int(hexval[:5], 16)
            dig_dir = hexval[5]
        else:
            dig_dir, dig_dist, _ = d.split(' ')
        match dig_dir:
            case 'U' | '3':
                y -= int(dig_dist)
            case 'D' | '1':
                y += int(dig_dist)
            case 'L' | '2':
                x -= int(dig_dist)
            case 'R' | '0':
                x += int(dig_dist)
        pts += [(x, y)]

    return pts

def part1_alt_polygon(output = True):
    pts = parse_pts(for_part2 = False)
    return int(polygon_grid_squares(pts))

def part2_alt_polygon(output = True):
    pts = parse_pts(for_part2 = True)
    return int(polygon_grid_squares(pts))

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 1:', part1_alt_floodfill(False), '(alternate method - flood fill)')
    print('Part 1:', part1_alt_polygon(False), '(alternate method - polygon area)')
    print('Part 2:', part2(True))
    print('Part 2:', part2_alt_polygon(False), '(alternate method - polygon area)')
