from collections import namedtuple
import re
import time

import mrm.ansi_term as ansi

with open('data/aoc_2018/17.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    rx = re.compile('([xy])=([0-9]+), ([xy])=([0-9]+)..([0-9]+)')
    clay = {}
    for d in dat:
        m = rx.match(d).groups()
        if m[0] == 'x':
            x = int(m[1])
            assert m[2] == 'y'
            for y in range(int(m[3]), int(m[4])+1):
                clay[(x, y)] = True
        else:
            assert m[0] == 'y' and m[2] == 'x'
            y = int(m[1])
            for x in range(int(m[3]), int(m[4]) + 1):
                clay[(x, y)] = True

    return clay

Point = namedtuple('Point', ['x', 'y'])
Range = namedtuple('Range', ['min', 'max'])

def print_section(clay, visited, drop_point, y_range):
    ansi.cursor_home()

    print(' '*120 + 'v--' + f'{drop_point.x:04d}')
    for y in range(drop_point.y - 25, drop_point.y + 25):
        for x in range(drop_point.x - 120, drop_point.x + 120):
            if y > y_range.max:
                print('=', end = '')
            elif x == drop_point.x and y == drop_point.y:
                print('o', end = '')
            elif (x, y) in clay:
                if clay[(x, y)]:
                    print(ansi.red('#'), end = '')
                else:
                    print(ansi.blue('~'), end = '')
            elif (x, y) in visited:
                print(ansi.green('|'), end = '')
            else:
                print(' ', end = '')
        print(f' [{y:04d}]', '**' if y == drop_point.y else '')
    time.sleep(0.01)

def drip(drop_point, clay, visited, y_range, output):
    drop_x, drop_y = drop_point

    if (drop_x, drop_y + 1) in visited:
        return

    while (drop_x, drop_y + 1) not in clay:
        drop_y += 1
        if y_range.min <= drop_y <= y_range.max:
            visited.add((drop_x, drop_y))
            if output:
                print_section(clay, visited, Point(drop_x, drop_y), y_range)
                print(len(visited))
        elif drop_y > y_range.max:
            return

    while True:
        visited.add((drop_x, drop_y))
        if output:
            print_section(clay, visited, Point(drop_x, drop_y), y_range)
            print(len(visited))

        new_lvl = [(drop_x, drop_y)]
        left_x = drop_x
        left_fall = None
        while (left_x - 1, drop_y) not in clay:
            left_x -= 1
            new_lvl += [(left_x, drop_y)]
            visited.add((left_x, drop_y))
            if (left_x, drop_y + 1) not in clay:
                left_fall = Point(left_x, drop_y)
                break

        right_x = drop_x
        right_fall = None
        while (right_x + 1, drop_y) not in clay:
            right_x += 1
            new_lvl += [(right_x, drop_y)]
            visited.add((right_x, drop_y))
            if (right_x, drop_y + 1) not in clay:
                right_fall = Point(right_x, drop_y)
                break

        if left_fall is not None or right_fall is not None:
            break

        for n in new_lvl:
            clay[n] = False
        drop_y -= 1

    if left_fall is not None:
        drip(left_fall, clay, visited, y_range, output)

    if right_fall is not None:
        drip(right_fall, clay, visited, y_range, output)

clay_change = 0

def part1(output = True):
    global clay_change

    clay = parse()
    spring = Point(500, 0)
    visited = set()
    min_y = min(clay.keys(), key = lambda x: x[1])[1]
    max_y = max(clay.keys(), key = lambda x: x[1])[1]
    y_range = Range(min_y, max_y)

    pre_clay = len(clay)
    if output:
        ansi.clear_screen()
        with ansi.hidden_cursor():
            drip(spring, clay, visited, y_range, True)
    else:
        drip(spring, clay, visited, y_range, False)
    post_clay = len(clay)
    clay_change = post_clay - pre_clay

    return len(visited)

def part2(output = True):
    if clay_change == 0:
        part1(False)

    return clay_change

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
