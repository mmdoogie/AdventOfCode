import re

import mrm.ansi_term as ansi

with open('data/aoc_2015/05.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    nice_strings = 0
    for d in dat:
        if any(x in d for x in ['ab', 'cd', 'pq', 'xy']):
            continue

        vowels = sum(x in 'aeiou' for x in d)
        if vowels < 3:
            continue

        pairs = sum(l * 2 in d for l in 'abcdefghijklmnopqrstuvwxyz')
        if pairs == 0:
            continue

        nice_strings += 1

    return nice_strings

def part2(output = True):
    pairs = re.compile(r'.*(.{2}).*\1')
    ahas = re.compile(r'.*((.).\2)')

    nice_strings = 0
    for d in dat:
        p = pairs.findall(d)
        if not p:
            continue

        a = ahas.findall(d)
        if not a:
            continue

        if output:
            print(d.replace(p[0], ansi.red(p[0])))
            print(d.replace(a[0][0], ansi.green(a[0][0])))
            print()

        nice_strings += 1

    return nice_strings

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
