from math import ceil, floor

import mrm.ansi_term as ansi

with open('data/aoc_2023/06.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def go_dist(time, button):
    return button * (time - button)

def part1(output = True):
    times = [int(x) for x in dat[0].split(':')[1].split(' ') if x != '']
    dists = [int(x) for x in dat[1].split(':')[1].split(' ') if x != '']

    if output:
        print('Times:', times)
        print('Dists:', dists)

    ways_all = 1
    for x in range(4):
        ways = 0
        t = times[x]
        d = dists[x]

        for button_time in range(t):
            g = go_dist(t, button_time)
            if g > d:
                ways += 1
        if output:
            print('Game', t, d, 'has', ways, 'ways')
        ways_all *= ways

    if output:
        print('All ways:', ways_all)

    return ways_all

def part2(output = True):
    time = int(dat[0].split(':')[1].replace(' ','').strip())
    dist = int(dat[1].split(':')[1].replace(' ','').strip())

    if output:
        print('Time:', time)
        print('Dist:', dist)

    # dist = button * (time - button)
    # dist = button * time - button^2
    # 0 = -1 * button^2 + time * button - dist
    a = -1
    b = time
    c = -dist

    coeff = (pow(b, 2) - 4 * a * c) / (4 * a * a)

    if output:
        print('a:', a)
        print('b:', b)
        print('c:', c)
        print(f'button times = ({int(-b / 2 / a)} +/- sqrt({int(coeff)}))')

    sol1 = -b / (2 * a) + pow(coeff, 0.5)
    sol2 = -b / (2 * a) - pow(coeff, 0.5)

    if sol1 > sol2:
        sol1, sol2 = sol2, sol1

    sol1 = ceil(sol1)
    sol2 = floor(sol2)

    assert go_dist(time, sol1) >= dist
    assert go_dist(time, sol1 - 1) < dist
    assert go_dist(time, sol2) >= dist
    assert go_dist(time, sol2 + 1) < dist

    if output:
        print(ansi.COLOR_RED + f'{sol1 - 1:>10d} goes', go_dist(time, sol1 - 1))
        print(ansi.COLOR_GREEN + f'{sol1:>10d} goes', go_dist(time, sol1))
        print(f'{sol2:>10d} goes', go_dist(time, sol2))
        print(ansi.COLOR_RED + f'{sol2 + 1:>10d} goes', go_dist(time, sol2 + 1), ansi.TEXT_RESET)

    return sol2 - sol1 + 1

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
