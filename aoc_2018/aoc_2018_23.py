from math import floor, ceil

with open('data/aoc_2018/23.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def manhat(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

def parse():
    scanners = []
    for d in dat:
        pos, rad = d.split(', ')
        pos = tuple(int(x) for x in pos.split('<')[1].split('>')[0].split(','))
        rad = int(rad.split('=')[1])
        scanners += [(pos, rad)]

    return scanners

def part1(output = True):
    scanners = parse()

    max_scanner = max(scanners, key = lambda x: x[1])
    if output:
        print('Scanner at', max_scanner[0], 'has max range, radius of', max_scanner[1])
    inrange_cnt = 0
    for s, _ in scanners:
        if manhat(max_scanner[0], s) <= max_scanner[1]:
            inrange_cnt += 1

    return inrange_cnt

def part2(output = True):
    scanners = parse()

    step = 10000000
    mini_scanners = [(tuple(ss/step for ss in s), r/step) for s, r in scanners]

    mins = {}
    maxs = {}
    for r in range(3):
        mins[r] = int(min(x[0][r] for x in mini_scanners))
        maxs[r] = int(max(x[0][r] for x in mini_scanners))

    if output:
        print('Scaling by', step)
        print(f'Searching range x={mins[0]} to {maxs[0]}, y={mins[1]} to {maxs[1]}, z={mins[2]} to {maxs[2]}')

    max_inrange = 0
    max_point = None
    for z in range(mins[2], maxs[2]):
        for y in range(mins[1], maxs[1]):
            for x in range(mins[0], maxs[0]):
                inrange = 0
                for ms, mr in mini_scanners:
                    if manhat((x, y, z), ms) <= mr:
                        inrange += 1
                if inrange > max_inrange:
                    max_inrange = inrange
                    max_point = (x, y, z)
                    if output:
                        print('Current max:', max_point, 'has in range', max_inrange)
    start_pt = [x * step for x in max_point]

    if output:
        print('New starting point:', start_pt)

    prev_step = step
    step = step / 10

    while step >= 1:
        mini_scanners = [([ss/step for ss in s], r/step) for s, r in scanners]

        for r in range(3):
            mins[r] = floor((start_pt[r] - 0.5 * prev_step) // step)
            maxs[r] = ceil((start_pt[r] + 0.5 * prev_step) // step)

        if output:
            print('Scale now', step)
            print(f'Searching range x={mins[0]} to {maxs[0]}, y={mins[1]} to {maxs[1]}, z={mins[2]} to {maxs[2]}')

        max_inrange = 0
        max_point = None
        min_dist_at_max = 1e20
        for z in range(mins[2], maxs[2]):
            for y in range(mins[1], maxs[1]):
                for x in range(mins[0], maxs[0]):
                    inrange = 0
                    for ms, mr in mini_scanners:
                        if manhat((x, y, z), ms) <= mr:
                            inrange += 1
                    if inrange >= max_inrange:
                        max_point = (x, y, z)
                        point_dist = sum(max_point)
                        if inrange > max_inrange:
                            min_dist_at_max = 1e20
                        if point_dist < min_dist_at_max:
                            min_dist_at_max = point_dist
                        max_inrange = inrange
                        if output:
                            print('Current max:', max_point, 'has in range', max_inrange, 'at dist', min_dist_at_max)

        if any(max_point[r] == mins[r] or max_point[r] == maxs[r] - 1 for r in range(3)):
            if output:
                print('Max was at edge -- redoing step')
            start_pt = [x * step for x in max_point]
        else:
            prev_step = step
            step = step / 10
            start_pt = [x * prev_step for x in max_point]

        if output:
            print('New starting point:', start_pt)

    inrange_cnt = 0
    for s, r in scanners:
        if manhat(start_pt, s) <= r:
            inrange_cnt += 1
    assert inrange_cnt == max_inrange
    assert manhat(start_pt, (0, 0, 0)) == min_dist_at_max

    return min_dist_at_max

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
