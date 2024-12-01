import itertools

with open('data/aoc_2018/02.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output = True):
    cnt_double = 0
    cnt_triple = 0

    for d in dat:
        if output:
            print(d, end='')
        has_double = 0
        has_triple = 0
        letters = set(list(d))
        for l in letters:
            letter_cnt = sum([c == l for c in d])
            if letter_cnt == 2:
                has_double = 1
                if output:
                    print(f' has 2 {l},', end='')
            if letter_cnt == 3:
                has_triple = 1
                if output:
                    print(f' has 3 {l},', end='')
        cnt_double += has_double
        cnt_triple += has_triple
        if output:
            print(f'  [{cnt_double}, {cnt_triple}]')
    return cnt_double * cnt_triple

def part2(output = True):
    for d1, d2 in itertools.combinations(dat, 2):
        mismatch = [a != b for a, b in zip(d1, d2)]
        diff_cnt = sum(mismatch)
        if output:
            print(f'{d1} vs {d2} has {diff_cnt} differences')
        if sum(mismatch) == 1:
            diff_loc = mismatch.index(True)
            return d1[:diff_loc] + d1[diff_loc+1:]
