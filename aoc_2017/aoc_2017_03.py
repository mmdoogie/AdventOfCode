from mrm.point import adj_diag

with open('data/aoc_2017/03.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    grid = int(dat[0])

def part1(output = True):
    closest_sqr = int(pow(grid, 0.5))
    remain = grid - pow(closest_sqr, 2)

    # odd squares are the bottom right corners of a grid of the square root size
    # center is 0, 0 so max x/y are half the square root size
    # the next step from here will expand the grid size and move to the right
    # even squares are one square away from the top left corner of the next larger grid
    # the next step from here will finish the row moving to the left
    if closest_sqr % 2 == 1:
        y = closest_sqr // 2
        x = y
        gm = y + 1
        dx, dy = 1, 0
    else:
        y = -closest_sqr // 2
        x = y + 1
        gm = -y
        dx, dy = -1, 0

    if output:
        print(f'Starting at {x:4}, {y:4}')
        print(f'Max grid {gm:4}')
        print(f'Next move direction {dx:2}, {dy:2}')

    while remain:
        if dx == 1:
            max_move = gm - x
            dist = min(remain, max_move)
            remain -= dist
            x += dist
            dx, dy = 0, -1
        elif dx == -1:
            max_move = -(-gm - x)
            dist = min(remain, max_move)
            remain -= dist
            x -= dist
            dx, dy = 0, 1
        elif dy == 1:
            max_move = gm - y
            dist = min(remain, max_move)
            remain -= dist
            y += dist
            dx, dy = 1, 0
        elif dy == -1:
            max_move = -(-gm - y)
            dist = min(remain, max_move)
            remain -= dist
            y -= dist
            dx, dy = -1, 0

        if output:
            print(f'\nRemaining in row/col {max_move:4}')
            print(f'Moved {dist:4}, remainder {remain:4}')
            if remain:
                print(f'Next move direction {dx:2}, {dy:2}')

    return abs(x) + abs(y)

def part2(output = True):
    del output

    x, y = 0, 0
    dx, dy = 1, 0
    gm = 1

    cells = {(0, 0): 1}

    while True:
        x += dx
        y += dy
        neigh = adj_diag((x, y), cells)
        new_val = sum(cells[n] for n in neigh)
        cells[(x, y)] = new_val
        if new_val > grid:
            break

        if dx == 1 and x == gm:
            dx, dy = 0, -1
        elif dx == -1 and x == -gm:
            dx, dy = 0, 1
        elif dy == 1 and y == gm:
            dx, dy = 1, 0
            gm += 1
        elif dy == -1 and y == -gm:
            dx, dy = -1, 0

    return new_val

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
