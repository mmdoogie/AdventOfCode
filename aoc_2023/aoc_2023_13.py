with open('data/aoc_2023/13.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def grids():
    blank_lines = [i for i, d in enumerate(dat) if d == ''] + [len(dat)]
    start = 0
    for b in blank_lines:
        yield dat[start:b]
        start = b + 1

def diff_cnt(l, r):
    return sum(a != b for a, b in zip(l, r))

def is_mirrored(grid, row, smudged = False):
    fixed = False
    for l, r in zip(grid[row::-1], grid[row + 1:]):
        if l != r:
            if not smudged:
                return False
            if diff_cnt(l, r) != 1 or fixed:
                return False
            fixed = True
    return fixed or not smudged

def transpose(grid):
    res = []
    for x in range(len(grid[0])):
        row = ''
        for y in range(len(grid)):
            row += grid[y][x]
        res += [row]
    return res

def summarize(grid, smudged = False):
    matched = [i for i, g_1 in enumerate(grid)
                 for j, g_2 in enumerate(grid)
                 if i != j and g_1 == g_2 and j - i == 1]
    for m in matched:
        if is_mirrored(grid, m, smudged):
            return 100 * (m + 1)

    if smudged:
        matched = [i for i, g_1 in enumerate(grid)
                     for j, g_2 in enumerate(grid)
                     if i != j and diff_cnt(g_1, g_2) == 1 and j - i == 1]
        for m in matched:
            if is_mirrored(grid, m, smudged):
                return 100 * (m + 1)

    t_grid = transpose(grid)

    matched = [i for i, g_1 in enumerate(t_grid)
                 for j, g_2 in enumerate(t_grid)
                 if i != j and g_1 == g_2 and j - i == 1]
    for m in matched:
        if is_mirrored(t_grid, m, smudged):
            return m + 1

    if smudged:
        matched = [i for i, g_1 in enumerate(t_grid)
                     for j, g_2 in enumerate(t_grid)
                     if i != j and diff_cnt(g_1, g_2) == 1 and j - i == 1]
        for m in matched:
            if is_mirrored(t_grid, m, smudged):
                return m + 1

    assert False
    return 0

def part1(output = True):
    return sum(summarize(g, smudged = False) for g in grids())

def part2(output = True):
    return sum(summarize(g, smudged = True) for g in grids())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
