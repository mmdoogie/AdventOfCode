from itertools import pairwise, islice

with open('data/aoc_2016/16.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    init = dat[0]

def inverted(data):
    return ['1' if d == '0' else '0' for d in data]

def checksum(data, maxlen):
    res = data[:maxlen]
    while True:
        res = ['1' if a[0]==a[1] else '0' for a in islice(pairwise(res), 0, None, 2)]
        if len(res) % 2 == 1:
            return ''.join(res)

def diskfill(size):
    data = list(init)
    while len(data) < size:
        data = data + ['0'] + inverted(reversed(data))
    return checksum(data, size)

def part1(output = True):
    del output
    return diskfill(272)

def part2(output = True):
    del output
    return diskfill(35651584)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
