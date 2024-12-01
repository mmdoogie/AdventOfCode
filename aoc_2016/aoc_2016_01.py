from time import sleep

import mrm.ansi_term as ansi
import mrm.cpoint as pt

with open('data/aoc_2016/01.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    steps = dat[0].split(', ')

def part1(output = True):
    pos = pt.ZERO
    head = pt.UP

    for s in steps:
        if s[0] == 'L':
            head = pt.left_turn(head)
        else:
            head = pt.right_turn(head)

        pos = pt.go_dist(pos, head, int(s[1:]))
        if output:
            print(s, '->', pt.as_xy(pos), 'dist', pt.m_dist(pos))

    return int(pt.m_dist(pos))

def viz(pos, seen, size=25):
    with ansi.hidden_cursor():
        with ansi.restored_cursor():
            for y in range(-size, size + 1):
                for x in range(-size*2, size*2 + 1):
                    dp = pt.from_xy(x, y) + pos
                    print('#' if dp in seen else ' ', end='')
                print()
            print(pt.as_xy(pos), 'dist', pt.m_dist(pos))

def part2(output = True):
    pos = pt.ZERO
    head = pt.UP
    seen = set()

    if output:
        ansi.clear_screen()
        ansi.save_cursor()

    for s in steps:
        if s[0] == 'L':
            head = pt.left_turn(head)
        else:
            head = pt.right_turn(head)

        for _ in range(int(s[1:])):
            pos = pt.go_dist(pos, head, 1)
            if output:
                viz(pos, seen)
                sleep(0.1)
            if pos in seen:
                if output:
                    print('during', s, 'revisited', pt.as_xy(pos), 'dist', pt.m_dist(pos))
                return int(pt.m_dist(pos))
            seen.add(pos)

    return 0

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
