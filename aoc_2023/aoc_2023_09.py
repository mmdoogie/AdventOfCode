from itertools import pairwise

import mrm.ansi_term as ansi

with open('data/aoc_2023/09.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    return [[int(x) for x in d.split(' ')] for d in dat]

def extrapolate(hist, backwards = False, output = True):
    if output:
        print()
        print(hist)

    diffs = [hist]
    curr_diff = hist
    while True:
        curr_diff = [b - a for a, b in pairwise(curr_diff)]
        diffs += [curr_diff]
        if output:
            print(curr_diff)
        if all(d == 0 for d in curr_diff):
            break

    val = 0
    for d in reversed(diffs):
        if not backwards:
            val = d[-1] + val
            if output:
                print('[' + ', '.join(str(x) for x in d) + ', ' + ansi.magenta(str(val)) + ']')
        else:
            val = d[0] - val
            if output:
                print('[' + ansi.magenta(str(val)) + ', ' + ', '.join(str(x) for x in d) + ']')
    if output:
        print('Extrapolated value:', val)

    return val

def part1(output = True):
    hists = parse()
    return sum(extrapolate(h, output = output) for h in hists)

def part2(output = True):
    hists = parse()
    return sum(extrapolate(h, backwards = True, output = output) for h in hists)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
