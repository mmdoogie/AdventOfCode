import mrm.ansi_term as ansi
import mrm.cpoint as cpt
import mrm.image as img

def parse():
    with open('data/aoc_2024/06.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def get_visited(grid, start):
    loc = start
    heading = cpt.UP
    visited = set()
    while True:
        if loc not in grid:
            return visited
        visited.add(loc)
        loc += heading
        if loc not in grid:
            return visited
        if grid[loc] == '#':
            loc -= heading
            heading = cpt.right_turn(heading)

def part1(output=False):
    lines = parse()
    grid = cpt.grid_as_dict(lines)
    start = [k for k, v in grid.items() if v == '^'][0]
    visited = get_visited(grid, start)
    if output:
        grid = {cpt.as_xy(k, int): v for k, v in grid.items()}
        img.print_image(grid, use_char=True, highlighter=lambda x, y, c: ansi.red('*') if cpt.from_xy(x, y) in visited else c)
    return len(visited)

def check_loop(grid, start, addin, max_loop):
    loc = start
    heading = cpt.UP
    visited = set()
    old_points = 0
    while True:
        if loc not in grid:
            return False
        if loc in visited:
            old_points += 1
        else:
            old_points = 0
            visited.add(loc)
        loc += heading
        if loc not in grid:
            return False
        if loc == addin or grid[loc] == '#':
            loc -= heading
            heading = cpt.right_turn(heading)
        if old_points > max_loop:
            return True

def part2(output=False):
    lines = parse()
    grid = cpt.grid_as_dict(lines)
    start = [k for k, v in grid.items() if v == '^'][0]
    visited = get_visited(grid, start)
    perim = (len(lines) + len(lines[0])) * 2
    return sum(check_loop(grid, start, v, perim) for v in visited)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
