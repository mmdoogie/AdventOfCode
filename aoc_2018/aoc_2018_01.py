import functools

with open('data/aoc_2018/01.txt') as f:
    dat = [x.strip() for x in f.readlines()]

vals = [int(d) for d in dat]

def part1(output = True):
    cs = functools.reduce(lambda a, b: a + b, vals)
    return cs

def part2(output = True):
    past_freqs = set([0])
    curr_freq = 0
    while True:
        for v in vals:
            curr_freq += v
            if curr_freq in past_freqs:
                return curr_freq
            past_freqs.add(curr_freq)

