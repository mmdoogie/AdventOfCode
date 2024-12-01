from collections import Counter
import re

import mrm.ansi_term as ansi

with open('data/aoc_2016/04.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    info_re = re.compile(r'([a-z-]+)([0-9]+)\[([a-z]+)\]')

def part1(output = True):
    total = 0
    for room in dat:
        info = info_re.match(room).groups()
        cnt = Counter(sorted(list(info[0])))
        del cnt['-']

        if ''.join(m[0] for m in cnt.most_common(5)) == info[2]:
            if output:
                print(ansi.green(room))
            total += int(info[1])
        elif output:
            print(ansi.red(room))

    return total

def part2(output = True):
    res = None
    for room in dat:
        info = info_re.match(room).groups()
        cnt = Counter(sorted(list(info[0])))
        del cnt['-']

        if ''.join(m[0] for m in cnt.most_common(5)) == info[2]:
            sid = int(info[1])
            key = {chr(ord('a') + a): chr(ord('a') + (a + sid) % 26) for a in range(26)}
            key['-'] = '-'
            decname = ''.join(key[a] for a in info[0])

            if decname.startswith('northpole'):
                res = sid
                if output:
                    print(ansi.green(decname[:-1]))
            elif output:
                print(ansi.red(decname[:-1]))

    return res

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
