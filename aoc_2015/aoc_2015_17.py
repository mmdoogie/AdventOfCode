from itertools import combinations

with open('data/aoc_2015/17.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    buckets = [int(x) for x in dat]

def part1(output = True):
    cnt = 0
    for n in range(len(buckets)):
        for cmb in combinations(buckets, n):
            if sum(cmb) == 150:
                cnt += 1
    return cnt

def part2(output = True):
    cnt = 0
    for n in range(len(buckets)):
        for cmb in combinations(buckets, n):
            if sum(cmb) == 150:
                cnt += 1
        if cnt > 0:
            return cnt
    return 0

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
