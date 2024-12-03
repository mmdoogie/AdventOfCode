import random

with open('data/aoc_2020/13.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output=False):
    min_time = int(dat[0])
    busses = [int(b) for b in dat[1].split(',') if b != 'x']

    waits = [b*(min_time // b + 1) - min_time for b in busses]
    min_waits = min(waits)

    return min_waits * busses[waits.index(min_waits)]

def part2(output=False):
    busses = [int(b) for b in dat[1].split(',') if b != 'x']
    offsets = [i for i, b in enumerate(dat[1].split(',')) if b != 'x']

    t = 0
    ts = busses[0]
    i = 1
    while i < len(busses):
        t += ts
        if output:
            print(t)
        
        if (t + offsets[i]) % busses[i] == 0:
            ts *= busses[i]
            i += 1

    return t
