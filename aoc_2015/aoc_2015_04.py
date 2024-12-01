from functools import partial
from itertools import count
from multiprocessing import Pool

from mrm.util import md5sum

with open('data/aoc_2015/04.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def compute(num_zeros):
    start_match = '0' * num_zeros
    key = dat[0]
    with Pool(8) as pool:
        it = pool.imap(partial(chk, start_match, key), count(), 1000)
        for val in it:
            if val is not None:
                return val

def chk(start_match, key, idx):
    digest = md5sum(key + str(idx))
    if digest.startswith(start_match):
        return idx
    return None

def part1(output = True):
    return compute(5)

def part2(output = True):
    return compute(6)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
