import mrm.ansi_term as ansi
import mrm.cpoint as cpt
import mrm.image as img

def parse():
    with open('data/aoc_2024/06.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return cpt.grid_as_dict(lines, with_inv=True)

def get_visited(grid, start):
    loc = start
    heading = cpt.UP
    visited = {(loc, heading): True}
    while True:
        if loc not in grid:
            return visited
        loc += heading
        if loc not in grid:
            return visited
        if grid[loc] == '#':
            loc -= heading
            heading = cpt.right_turn(heading)
            continue
        visited[(loc, heading)] = True

def part1(output=False):
    grid, inv = parse()
    start = inv['^'].pop()
    visited = set(k[0] for k in get_visited(grid, start))
    if output:
        img.print_image(grid, use_char=True, highlighter=lambda x, y, c: ansi.red('*') if cpt.from_xy(x, y) in visited else c)
    return len(visited)

def check_loop(grid, start, pre_visited, addin):
    loc = start[0]
    heading = start[1]
    visited = set()
    while True:
        if loc not in grid:
            return False
        loc += heading
        if loc not in grid:
            return False
        if loc == addin or grid[loc] == '#':
            loc -= heading
            heading = cpt.right_turn(heading)
            continue
        if (loc, heading) in visited or (loc, heading) in pre_visited:
            return True
        visited.add((loc, heading))

def part2(output=False):
    grid, inv = parse()
    start = inv['^'].pop()
    visited = list(get_visited(grid, start).keys())
    visited_points = [k[0] for k in visited]

    obstrs = {vp: visited_points.index(vp) for vp in visited_points}
    total = 0
    visited_so_far = set()
    vsf_idx = -1
    for ob_pt, ob_idx in obstrs.items():
        if ob_pt == start:
            continue
        visited_so_far.update(visited[vsf_idx:ob_idx])
        vsf_idx = ob_idx
        total += check_loop(grid, visited[ob_idx - 1], visited_so_far, ob_pt)
    return total

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
