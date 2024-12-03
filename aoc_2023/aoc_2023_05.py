import mrm.ansi_term as ansi

with open('data/aoc_2023/05.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def apply_maps(maps, seed):
    pre_map = seed
    for m in maps:
        for ds, ss, rl in m:
            if ss <= pre_map < ss + rl:
                pre_map = ds + (pre_map - ss)
                break
    return pre_map

def parse(seed_ranges = False):
    seeds = [int(x) for x in dat[0].split(': ')[1].split(' ')]

    if seed_ranges:
        seeds = [(seeds[2 * i], seeds[2 * i + 1]) for i in range(len(seeds) // 2)]

    maps = []
    curr_map = []
    for d in dat[3:]:
        if d == '':
            continue
        if ':' in d:
            maps += [curr_map]
            curr_map = []
        else:
            curr_map += [tuple(int(x) for x in d.split(' '))]

    maps += [curr_map]

    return seeds, maps

def part1(output = True):
    seeds, maps = parse(seed_ranges = False)
    locs = {apply_maps(maps, s): s for s in seeds}
    min_loc = min(locs.keys())

    if output:
        for lk, lv in locs.items():
            if lk == min_loc:
                print(ansi.COLOR_GREEN, end='')
            print(f'Seed {lv:<10d} maps to location {lk}')
            if lk == min_loc:
                print(ansi.TEXT_RESET, end='')

    return min_loc

def split_ranges(in_ranges, trans_map):
    unsplit = in_ranges
    out_ranges = []

    for map_dest, map_src, map_len in trans_map:
        map_end = map_src + map_len - 1
        map_adj = map_dest - map_src
        next_unsplit = []
        for rng_src, rng_len in unsplit:
            rng_end = rng_src + rng_len - 1
            if rng_src <= map_src <= rng_end:
                split_start = map_src
            elif map_src <= rng_src <= map_end:
                split_start = rng_src
            else:
                next_unsplit += [(rng_src, rng_len)]
                continue

            if rng_src <= map_end <= rng_end:
                split_end = map_end
            elif map_src <= rng_end <= map_end:
                split_end = rng_end
            else:
                next_unsplit += [(rng_src, rng_len)]
                continue

            out_ranges += [(split_start + map_adj , split_end - split_start + 1)]

            if split_start > rng_src:
                next_unsplit += [(rng_src, split_start - rng_src + 1 - 1)]
            if split_end < rng_end:
                next_unsplit += [(split_end + 1, rng_end - split_end - 1 + 1)]
        unsplit = next_unsplit

    return out_ranges

def part2(output = True):
    seeds, maps = parse(seed_ranges = True)
    curr_ranges = seeds

    if output:
        print('Seed ranges')
        print(curr_ranges)
        print()

    for i, m in enumerate(maps):
        curr_ranges = split_ranges(curr_ranges, m)
        if output:
            print('After map', i + 1)
            print(curr_ranges)
            print()

    return sorted(curr_ranges)[0][0]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
