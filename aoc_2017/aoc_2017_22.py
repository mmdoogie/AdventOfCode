from time import sleep

import mrm.ansi_term as ansi
from mrm.point import grid_as_dict

with open('data/aoc_2017/22.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def viz(grid, x0, y0, burst, space=25):
    with ansi.hidden_cursor():
        ansi.cursor_home()
        for y in range(y0-space, y0+space):
            for x in range(x0-2*space, x0+2*space):
                gv = grid.get((x, y), '.')
                if x == x0 and y == y0:
                    cfun = ansi.magenta
                elif gv == '#':
                    cfun = ansi.red
                elif gv == '~':
                    cfun = ansi.yellow
                elif gv == '@':
                    cfun = ansi.blue
                else:
                    cfun = ansi.green
                print(cfun(gv), end='')
            print()
        print('Burst:', burst + 1)
        if burst < 200:
            sleep(0.05)

def part1(output = True):
    grid = grid_as_dict(dat)
    x = len(dat[0]) // 2
    y = len(dat) // 2
    dx = 0
    dy = -1

    if output:
        ansi.clear_screen()

    infecting_bursts = 0
    for r in range(10000):
        infected = grid.get((x, y), '.') == '#'

        if infected:
            if dx == 1:
                dx = 0
                dy = 1
            elif dx == -1:
                dx = 0
                dy = -1
            elif dy == 1:
                dx = -1
                dy = 0
            else:
                dx = 1
                dy = 0
        else:
            if dx == 1:
                dx = 0
                dy = -1
            elif dx == -1:
                dx = 0
                dy = 1
            elif dy == 1:
                dx = 1
                dy = 0
            else:
                dx = -1
                dy = 0

        grid[(x, y)] = '.' if infected else '#'
        if not infected:
            infecting_bursts += 1

        if output:
            viz(grid, x, y, r)

        x += dx
        y += dy

    return infecting_bursts

def part2(output = True):
    grid = grid_as_dict(dat)
    x = len(dat[0]) // 2
    y = len(dat) // 2
    dx = 0
    dy = -1

    if output:
        ansi.clear_screen()

    infecting_bursts = 0
    for r in range(10000000):
        gv = grid.get((x, y), '.')

        cleaned = gv == '.'
        infected = gv == '#'
        weakened = gv == '~'
        flagged = gv == '@'

        if infected:
            if dx == 1:
                dx = 0
                dy = 1
            elif dx == -1:
                dx = 0
                dy = -1
            elif dy == 1:
                dx = -1
                dy = 0
            else:
                dx = 1
                dy = 0
        if cleaned:
            if dx == 1:
                dx = 0
                dy = -1
            elif dx == -1:
                dx = 0
                dy = 1
            elif dy == 1:
                dx = 1
                dy = 0
            else:
                dx = -1
                dy = 0
        if flagged:
            dx = -dx
            dy = -dy

        if cleaned:
            grid[(x, y)] = '~'
        elif weakened:
            grid[(x, y)] = '#'
            infecting_bursts += 1
        elif infected:
            grid[(x, y)] = '@'
        else:
            grid[(x, y)] = '.'

        if output and r%10000 == 0:
            viz(grid, x, y, r)
            sleep(0.1)

        x += dx
        y += dy

    return infecting_bursts

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
