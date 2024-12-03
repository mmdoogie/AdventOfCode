from functools import cache

with open('data/aoc_2023/14.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def rotate_left(grid):
    res = []
    width = len(grid[0])
    for x in range(width):
        row = ''
        for y in range(len(grid)):
            row += grid[y][width - 1 - x]
        res += [row]

    return tuple(res)

@cache
def rotate_right(grid):
    res = []
    height = len(grid)
    for x in range(len(grid[0])):
        row = ''
        for y in range(height):
            row += grid[height - 1 - y][x]
        res += [row]

    return tuple(res)

@cache
def tilt_left(grid):
    tilted_grid = []
    width = len(grid[0])
    for row in grid:
        stoppers = [-1]
        row_score = []
        count = 1
        for i, c in enumerate(row):
            if c == '#':
                stoppers += [i]
                count = 1
            elif c == 'O':
                row_score += [width - (stoppers[-1] + count)]
                count += 1
        new_row = ''
        for x in range(width):
            if x in stoppers:
                new_row += '#'
            elif width - x in row_score:
                new_row += 'O'
            else:
                new_row += '.'
        tilted_grid += [new_row]

    return tuple(tilted_grid)

@cache
def score_grid(grid):
    return sum(len(grid[0]) - i for row in grid for i, c in enumerate(row) if c == 'O')

def part1(output = True):
    rotated_grid = rotate_left(dat)
    tilted_grid = tilt_left(rotated_grid)
    return score_grid(tilted_grid)

def part2(output = True):
    score_hist = []
    rotated_grid = rotate_left(dat)
    for it in range(250):
        for _ in range(4):
            tilted_grid = tilt_left(rotated_grid)
            rotated_grid = rotate_right(tilted_grid)
        score = score_grid(rotated_grid)
        if output:
            print(f'Cycle: {it + 1:3d}     Score: {score:6d}')
        score_hist += [score]

    offset = -1
    while score_hist[offset + 1:] != score_hist[2 * (offset + 1):offset + 1]:
        offset -= 1
        while score_hist[offset] != score_hist[-1]:
            offset -= 1

    cycle_len = -offset - 1
    target = 1000000000
    if output:
        print('Pattern found with length', cycle_len)
        print('Last', cycle_len, 'values:', score_hist[offset + 1:])
        print('Prev', cycle_len, 'values:', score_hist[2 * (offset + 1):offset + 1])
        print()
        print('Target cycle count:', target)

    target -= len(score_hist)
    if output:
        print('Remaining:', target)
        print(f'Skipping {target // cycle_len} patterns ({cycle_len * (target // cycle_len)} iterations)')

    target -= cycle_len * (target // cycle_len)
    if output:
        print('Remaining:', target)

    return score_hist[offset + target]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
