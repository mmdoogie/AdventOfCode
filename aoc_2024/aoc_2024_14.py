from collections import Counter
from functools import reduce
import operator

from mrm.ansi_term import red, green
from mrm.crt import crt
from mrm.graph import connected_component
import mrm.image as img
from mrm.parse import all_nums
from mrm.point import adj_ortho

def parse():
    with open('data/aoc_2024/14.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    robots = [tuple(all_nums(l)) for l in lines]
    return robots

WIDTH = 101
HEIGHT = 103

def robots_at_time(robots, time):
    return [((r[0] + time * r[2]) % WIDTH, (r[1] + time * r[3]) % HEIGHT) for r in robots]

def part1(output=False):
    robots = parse()

    at_end = robots_at_time(robots, 100)

    def quad(r):
        if r[0] < WIDTH // 2:
            if r[1] < HEIGHT // 2:
                return 1
            if r[1] > HEIGHT // 2:
                return 2
        if r[0] > WIDTH // 2:
            if r[1] < HEIGHT // 2:
                return 3
            if r[1] > HEIGHT // 2:
                return 4
        return 0

    qcnt = Counter(quad(r) for r in at_end)
    return reduce(operator.mul, (v for k, v in qcnt.items() if k != 0))

def part2(output=False):
    robots = parse()

    sec = 1
    rem_c40 = None
    mod_c40 = None
    rem_r36 = None
    mod_r36 = None
    while True:
        at_end = robots_at_time(robots, sec)

        c40 = [r for r in at_end if r[0] == 40]
        if len(c40) > 20:
            if not rem_c40:
                rem_c40 = sec
            elif not mod_c40:
                mod_c40 = sec - rem_c40

        r36 = [r for r in at_end if r[1] == 36]
        if len(r36) > 20:
            if not rem_r36:
                rem_r36 = sec
            elif not mod_r36:
                mod_r36 = sec - rem_r36

        if rem_c40 and mod_c40 and rem_r36 and mod_r36:
            break

        sec += 1

    sec = crt([rem_c40, rem_r36], [mod_c40, mod_r36])
    at_end = robots_at_time(robots, sec)

    if output:
        ngh = {r: adj_ortho(r, at_end) for r in at_end}
        border = connected_component(ngh, (40, 36))
        tree = connected_component(ngh, (50, 50))
        def highlighter(x, y, c):
            if (x, y) in border:
                return red(c)
            if (x, y) in tree:
                return green(c)
            return c
        img.print_image({a: '*' for a in at_end}, use_char=True, highlighter=highlighter, border=True)
        print(f't: {sec} --> {sec} % {mod_c40} = {rem_c40} && {sec} % {mod_r36} = {rem_r36}')

    return sec

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
