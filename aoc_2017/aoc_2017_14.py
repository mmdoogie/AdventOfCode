from mrm.point import adj_ortho, grid_as_dict
from aoc_2017 import aoc_2017_10

with open('data/aoc_2017/14.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    HTOB = {f'{h:01x}': f'{h:04b}' for h in range(16)}

def part1(output = True):
    key = dat[0]
    total = 0

    for row in range(128):
        row_key = f'{key}-{row}'
        hash_str = aoc_2017_10.knot_hash(row_key)
        row_bin = ''.join([HTOB[c] for c in hash_str])
        total += sum(int(c) for c in row_bin)
        if output:
            print(f'{row_key:12} {hash_str} {row_bin}')

    return total

def part2(output = True):
    key = dat[0]
    grid = []

    for row in range(128):
        hash_str = aoc_2017_10.knot_hash(f'{key}-{row}')
        row_bin = ''.join([HTOB[c] for c in hash_str])
        grid += [[int(c) for c in row_bin]]

    d = grid_as_dict(grid, lambda x: x == 1)
    all_pts = set(d.keys())

    regions = 0
    while all_pts:
        seed = all_pts.pop()
        in_region = {seed}
        to_chk = {seed}

        while to_chk:
            is_at = to_chk.pop()
            ngh = adj_ortho(is_at, d)
            for n in ngh:
                if n not in in_region:
                    to_chk.add(n)
                    in_region.add(n)

        all_pts -= in_region
        regions += 1

        if output:
            print(f'Region {regions} from seed {seed} contains {len(in_region)} points, remaining {len(all_pts)}')

    return regions

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
