from mrm.point import grid_as_dict, adj_diag

with open('data/aoc_2015/18.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    grid = set(grid_as_dict(dat, lambda x: x == '#'))
    width = len(dat[0])
    height = len(dat)

    for _ in range(100):
        add = set()
        remove = set()
        for y in range(height):
            for x in range(width):
                at_pt = (x, y)
                ngh = len(adj_diag(at_pt, grid))
                if at_pt in grid:
                    if ngh < 2 or ngh > 3:
                        remove.add(at_pt)
                else:
                    if ngh == 3:
                        add.add(at_pt)
        grid -= remove
        grid |= add
    return len(grid)

def part2(output = True):
    grid = set(grid_as_dict(dat, lambda x: x == '#'))
    width = len(dat[0])
    height = len(dat)
    stuck = set([(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)])
    grid |= stuck

    for _ in range(100):
        add = set()
        remove = set()
        for y in range(height):
            for x in range(width):
                at_pt = (x, y)
                ngh = len(adj_diag(at_pt, grid))
                if at_pt in grid:
                    if ngh < 2 or ngh > 3:
                        remove.add(at_pt)
                else:
                    if ngh == 3:
                        add.add(at_pt)
        grid -= remove
        grid |= add
        grid |= stuck
    return len(grid)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
