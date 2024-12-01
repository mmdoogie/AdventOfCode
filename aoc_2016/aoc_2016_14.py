from collections import deque
from hashlib import md5
import re

with open('data/aoc_2016/14.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    salt = dat[0]

triplet_re = re.compile(r'(.)\1{2}')
def check_triplet(s):
    fnd = triplet_re.findall(s)
    if fnd:
        return fnd[0]
    return None

quintlet_re = re.compile(r'(.)\1{4}')
def check_quintlet(s):
    fnd = quintlet_re.findall(s)
    if fnd:
        return fnd[0]
    return None

def md5_1x(val):
    return md5(val.encode('utf-8')).hexdigest()

def super_md5(val):
    x = val
    for _ in range(2017):
        x = md5(x.encode('utf-8')).hexdigest()
    return x

def process(md5fun, output):
    genidx = 0
    hashes = deque()
    key_idx = []

    while len(key_idx) < 64:
        if hashes:
            idx, chk = hashes.popleft()
        else:
            idx = genidx
            chk = md5fun(salt + str(idx))
            genidx += 1

        t = check_triplet(chk)
        if output and t:
            print(f'{salt}{idx:<5} = {chk} T{t}', end=' ')
        if not t:
            continue
        t_idx = idx

        while len(hashes) < 1000:
            idx = genidx
            chk = md5fun(salt + str(idx))
            genidx += 1
            hashes.append((idx, chk))

        assert len(hashes) == 1000

        k_add = False
        for idx, chk in hashes:
            q = check_quintlet(chk)
            if q == t:
                key_idx += [t_idx]
                if output:
                    print(f'K{len(key_idx)}')
                k_add = True
                break
        if output and not k_add:
            print()

    return key_idx[63]

def part1(output = True):
    return process(md5_1x, output)

def part2(output = True):
    return process(super_md5, output)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
