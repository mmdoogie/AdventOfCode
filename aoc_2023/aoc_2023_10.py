import mrm.ansi_term as ansi
from mrm.image import minmax_x, minmax_y, print_image
from mrm.point import adj_ortho, point_add, point_sub, ZERO_2D

with open('data/aoc_2023/10.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    tiles = {}
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            tiles[(x, y)] = c
            if c == 'S':
                start = (x, y)

    return tiles, start

def extract_loop(start, tiles, output = True):
    connected = {'|': [( 0, 1), (0, -1)],
                 '-': [(-1, 0), (1,  0)],
                 'L': [(-1, 0), (0,  1)],
                 'J': [( 1, 0), (0,  1)],
                 '7': [( 1, 0), (0, -1)],
                 'F': [(-1, 0), (0, -1)],
                 '.': [],
                 'S': []}
    path_points = [start]
    in_path = set(path_points)

    for adj_dir in adj_ortho(ZERO_2D):
        adj_pt = point_add(start, adj_dir)
        if adj_dir in connected[tiles[adj_pt]]:
            in_path.add(adj_pt)
            path_points += [adj_pt]
            break
    if output:
        print('Traversing loop via:', path_points[-1])
        print('S' + tiles[path_points[-1]], end = '')

    while True:
        for conn_dir in connected[tiles[path_points[-1]]]:
            try_point = point_sub(path_points[-1], conn_dir)
            if try_point not in in_path:
                in_path.add(try_point)
                path_points += [try_point]
                if output:
                    print(tiles[try_point], end = '')
                break
            if try_point == start and len(in_path) != 2:
                break
        if try_point == start and len(in_path) != 2:
            break
    if output:
        print('S')
        print('Returned to start, loop complete! Total path length:', len(in_path))

    shape_fig = {point_sub(*sorted(v)): k for k, v in connected.items() if len(v) == 2}
    start_shape = point_sub(*sorted([path_points[1], path_points[-1]]))
    start_fig = shape_fig[start_shape]

    return path_points, start_fig

def part1(output = True):
    tiles, start = parse()
    if output:
        print('Start location:', start)

    path, _ = extract_loop(start, tiles, output)

    return len(path) // 2

def inside_polygon_row(path_tiles, y, min_x, max_x):
    cross_cnt = 0
    prev_tile = False

    counts = []
    for x in range(min_x, max_x + 1):
        if (x, y) in path_tiles:
            curr_tile = path_tiles[(x, y)]
            if prev_tile == 'F' and curr_tile in 'J7':
                if curr_tile == 'J':
                    cross_cnt += 1
                prev_tile = False
            elif prev_tile == 'L' and curr_tile in 'J7':
                if curr_tile == '7':
                    cross_cnt += 1
                prev_tile = False
            elif curr_tile == '|':
                assert not prev_tile
                cross_cnt += 1
            elif curr_tile not in '-J7@':
                prev_tile = curr_tile
        counts += [cross_cnt]
    return counts

def part2(output = True):
    tiles, start = parse()
    path, start_fig = extract_loop(start, tiles, False)

    path_tiles = {p: tiles[p] for p in path}
    path_tiles[start] = start_fig
    if output:
        print('Extracted loop:')
        print_image(path_tiles, True)

    enclosed_cnt = 0
    min_x, max_x = minmax_x(path)
    min_y, max_y = minmax_y(path)

    for y in range(min_y, max_y + 1):
        cross_counts = inside_polygon_row(path_tiles, y, min_x, max_x)
        for x in range(min_x, max_x + 1):
            if (x, y) in path_tiles:
                continue
            if cross_counts[x - min_x] % 2:
                path_tiles[(x, y)] = '@'
                enclosed_cnt += 1

    if output:
        print('Enclosed locations highlighted:')
        char_swap = {'F': '\u250c', 'J': '\u2518',
                     '7': '\u2510', 'L': '\u2514',
                     '-': '\u2500', '|': '\u2502',
                     'S': 'x',      '@': 'o'}
        pretty_tiles = {p: char_swap[path_tiles[p]] for p in path_tiles}
        pretty_tiles[start] = ansi.yellow('x')
        print_image(pretty_tiles, True, '\u00b7', lambda x, y, c: ansi.magenta(c) if c == 'o' else c)

    return enclosed_cnt

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
