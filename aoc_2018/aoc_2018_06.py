with open('data/aoc_2018/06.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def mdist(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def part1(output = True):
    centers = [tuple([int(x) for x in l.split(', ')]) for l in dat]
    min_x = min(centers, key = lambda x: x[0])[0]
    max_x = max(centers, key = lambda x: x[0])[0]
    min_y = min(centers, key = lambda x: x[1])[1]
    max_y = max(centers, key = lambda x: x[1])[1]
    if output:
        print(f'{len(centers)} cell centers')
        print(f'X range: {min_x} to {max_x}')
        print(f'Y range: {min_y} to {max_y}')
    
    closest = {}
    sizes = {}
    outside_cells = set()
    for y in range(min_y - 50, max_y + 50 + 1):
        for x in range(min_x - 50, max_x + 50 + 1):
            pt = (x, y)
            dists = [mdist(pt, c) for c in centers]
            min_dist = min(dists)
            ci = dists.index(min_dist)
            if min_dist in dists[ci+1:]:
                continue
            closest[pt] = ci
            cn = centers[ci]
            if x == min_x - 50 or x == max_x + 50 or y == min_y - 50 or y == max_y + 50:
                outside_cells.add(cn)
            if cn not in sizes:
                sizes[cn] = 1
            else:
                sizes[cn] += 1

    sizes = sorted(sizes.items(), key = lambda x: x[1], reverse = True)

    if output:
        for y in range(min_y - 50, max_y + 50 + 1):
            for x in range(min_x - 50, max_x + 50 + 1):
                if (x, y) in centers:
                    if (x, y) in outside_cells:
                        print('o', end='')
                    else:
                        print('x', end='')
                elif (x, y) in closest:
                    print(chr(closest[(x,y)] + ord('A')), end='')
                else:
                    print(' ', end='');
            print()

    valid_sizes = sorted({k: v for k, v in sizes if k not in outside_cells}.items(), key = lambda x: x[1], reverse = True)

    if output:
        print('Largest cells:', sizes[:6])
        print('Outside cells:', len(outside_cells), 'of', len(centers), outside_cells)
        print('Non-outside largest cells:', valid_sizes[:6])

    return valid_sizes[0][1]

def part2(output = True):
    centers = [tuple([int(x) for x in l.split(', ')]) for l in dat]
    min_x = min(centers, key = lambda x: x[0])[0]
    max_x = max(centers, key = lambda x: x[0])[0]
    min_y = min(centers, key = lambda x: x[1])[1]
    max_y = max(centers, key = lambda x: x[1])[1]
    
    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2

    less_cnt = 0
    min_dist = 10000
    max_dist = 0
    for dy in range(max_y - cy):
        for dx in range(max_x - cx):
            pts = set([(cx - dx, cy - dy), (cx - dx, cy + dy), (cx + dx, cy - dy), (cx + dx, cy + dy)])
            dists = [sum([mdist(p, c) for c in centers]) for p in pts]
            less_cnt += sum([d < 10000 for d in dists])
            if output:
                if min(dists) < min_dist:
                    min_dist = min(dists)
                if max(dists) > max_dist:
                    max_dist = max(dists)
            if all([d >= 10000 for d in dists]):
                break
        if dy == 0:
            assert dx < max_x - cx
        if dx == 0:
            break
    assert dy < max_y - cy

    if output:
        print(f'Min dist: {min_dist}, Max dist: {max_dist}')
    
    return less_cnt
