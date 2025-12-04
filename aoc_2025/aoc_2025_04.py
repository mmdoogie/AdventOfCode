import mrm.point as pt
import mrm.image as img
import mrm.ansi_term as ansi

def parse():
    with open('data/aoc_2025/04.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = set(pt.grid_as_dict(lines, lambda x: x == '@'))
    return grid

def part1(output=False):
    grid = parse()

    rem = set(g for g in grid if len(pt.adj_diag(g, grid)) < 4)

    if output:
        img.print_image({g: '@' for g in grid}, True, highlighter=lambda x, y, c: ansi.red(c) if (x, y) in rem else c)

    return len(rem)

def part2(output=False):
    grid = parse()
    start_grid = set(grid)

    while True:
        rem = set(g for g in grid if len(pt.adj_diag(g, grid)) < 4)
        grid = grid.difference(rem)
        if not rem:
            break

    if output:
        img.print_image({g: '@' for g in start_grid}, True, highlighter=lambda x, y, c: ansi.red(c) if (x, y) not in grid else c)

    return len(start_grid) - len(grid)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
