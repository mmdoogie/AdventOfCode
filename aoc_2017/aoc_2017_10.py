from functools import reduce
from operator import xor

with open('data/aoc_2017/10.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    LOOP_SIZE = 256

def apply_lens(marks, lens, pos = 0, skip_size = 0):
    for l in lens:
        if pos + l <= LOOP_SIZE:
            marks = marks[:pos] + list(reversed(marks[pos:pos + l])) + marks[pos + l:]
        else:
            wrap = pos + l - LOOP_SIZE
            sub_list = list(reversed(marks[pos:] + marks[:wrap]))
            marks = sub_list[-wrap:] + marks[wrap:pos] + sub_list[:-wrap]
        pos = (pos + l + skip_size) % LOOP_SIZE
        skip_size += 1

    return marks, pos, skip_size

def part1(output = True):
    del output

    lens = [int(x) for x in dat[0].split(',')]
    marks, _, _ = apply_lens(list(range(LOOP_SIZE)), lens)
    return marks[0] * marks[1]

def knot_hash(txt):
    lens = [ord(x) for x in txt] + [17,31,73,47,23]

    marks = list(range(LOOP_SIZE))
    pos = 0
    skip_size = 0

    for _round in range(64):
        marks, pos, skip_size = apply_lens(marks, lens, pos, skip_size)

    results = []
    for i in range(16):
        sub_list = marks[i*16:(i+1)*16]
        results += [reduce(xor, sub_list)]

    return ''.join(f'{x:02x}' for x in results)

def part2(output = True):
    del output

    return knot_hash(dat[0])

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
