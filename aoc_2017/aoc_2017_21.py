with open('data/aoc_2017/21.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    pats = {}
    for d in dat:
        in_pat, out_pat = d.split(' => ')
        pats[in_pat] = out_pat

def subdivide(grid):
    width = len(grid[0])
    height = len(grid)

    res = []
    if width % 2 == 0:
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                res += [[grid[y][x:x+2], grid[y+1][x:x+2]]]
        return res

    assert width % 3 == 0
    for y in range(0, height, 3):
        for x in range(0, width, 3):
            res += [[grid[y][x:x+3], grid[y+1][x:x+3], grid[y+2][x:x+3]]]
    return res

def isomorphs(grid):
    res = [grid]

    # flip y
    res += [grid[-1:-len(grid)-1:-1]]

    # flip x
    res += [[g[-1:-len(grid)-1:-1] for g in grid]]

    # rotate 180 = flip x + flip y
    res += [[g[-1:-len(grid)-1:-1] for g in grid[-1:-len(grid)-1:-1]]]

    # rotate right
    add = []
    for y in range(len(grid)):
        add += [''.join([g[y] for g in grid[-1:-len(grid)-1:-1]])]
    res += [add]
    # then flip y
    res += [add[-1:-len(grid)-1:-1]]

    # rotate left
    add = []
    for y in range(len(grid)):
        add += [''.join([g[len(grid)-1-y] for g in grid])]
    res += [add]
    # then flip y
    res += [add[-1:-len(grid)-1:-1]]

    return ['/'.join(r) for r in res]

def combine(res):
    parts = len(res)
    if parts == 1:
        return res[0]

    amt = int(pow(parts, 0.5))

    combo = []
    for a in range(0, parts, amt):
        combo += [''.join(l) for l in zip(*res[a:a+amt])]

    return combo

def compute(output, grid, iterations):
    isopats = {}
    for pk, pv in pats.items():
        isos = isomorphs(pk.split('/'))
        isopats.update({i: pv for i in isos})

    for it in range(iterations):
        if output:
            print('Iteration:', it + 1)
        s = subdivide(grid)
        res = []
        for sg in s:
            op = isopats['/'.join(sg)]
            res += [op]
            if output:
                print('sg >', sg, '>', op)
        grid = combine([r.split('/') for r in res])

    return sum(c == '#' for g in grid for c in g)

def part1(output = True):
    grid = ['.#.', '..#', '###']
    return compute(output, grid, 5)

def part2(output = True):
    grid = ['.#.', '..#', '###']
    return compute(output, grid, 18)

if __name__ == '__main__':
    print('Part 1:', part1(False))
    print('Part 2:', part2(False))
