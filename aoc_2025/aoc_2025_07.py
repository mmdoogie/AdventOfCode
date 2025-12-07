import mrm.ansi_term as ansi
from mrm.cache import Keycache
import mrm.image as img
import mrm.point as pt

def parse():
    with open('data/aoc_2025/07.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid, inv = pt.grid_as_dict(lines, with_inv=True)
    return grid, inv['S'].pop()

def part1(output=False):
    grid, start_pt = parse()
    max_y = max(g[1] for g in grid)

    beams = set([start_pt])
    splits = 0
    for y in range(start_pt[1] + 1, max_y):
        new_beams = {(b[0], y) for b in beams}
        del_beams = {b for b in new_beams if grid[b] == '^'}
        add_beams_left  = {(b[0] - 1, b[1]) for b in del_beams}
        add_beams_right = {(b[0] + 1, b[1]) for b in del_beams}
        splits += len(del_beams)
        beams = (new_beams - del_beams) | add_beams_left | add_beams_right
        if output:
            for b in beams:
                grid[b] = ansi.green('|')

    if output:
        img.print_image(grid, True)

    return splits

def part2(output=False):
    grid, start_pt = parse()
    max_y = max(g[1] for g in grid)

    @Keycache(stats=True)
    def dfs(from_pt, *, key):
        while grid[from_pt] != '^':
            from_pt = (from_pt[0], from_pt[1] + 1)
            if from_pt[1] > max_y:
                return 1
        left_pt  = (from_pt[0] - 1, from_pt[1])
        right_pt = (from_pt[0] + 1, from_pt[1])
        return dfs(left_pt, key=left_pt) + dfs(right_pt, key=right_pt)

    ends = dfs(start_pt, key=start_pt)

    if output:
        hits, misses = dfs.stats()
        print(f'DFS Cache: {hits} hits, {misses} misses, {hits/(hits+misses)*100:.2f}% hit ratio')

    return ends

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
