from collections import Counter

with open('data/aoc_2016/06.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    cnts = [Counter(d[c] for d in dat) for c in range(len(dat[0]))]

def part1(output = True):
    del output
    return ''.join(c.most_common()[0][0] for c in cnts)

def part2(output = True):
    del output
    return ''.join(c.most_common()[-1][0] for c in cnts)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
