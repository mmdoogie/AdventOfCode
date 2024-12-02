from itertools import chain, repeat, cycle, islice, accumulate
import operator

def parse():
    with open('data/aoc_2019/16.txt') as f:
        dat = [x.strip() for x in f.readlines()]
    inp = [int(d) for d in dat[0]]
    return inp, int(dat[0][0:7])

def place_iter(place):
    return islice(cycle(chain(repeat(0, place), repeat(1, place), repeat(0, place), repeat(-1, place))), 1, None)

def phase(inp):
    return [abs(sum([a*b for a,b in zip(place_iter(p+1), inp)])) % 10 for p in range(len(inp))]

def part1(output=False):
    inp, _ = parse()
    for r in range(100):
        inp = phase(inp)
    return ''.join(str(x) for x in inp[0:8])

def part2(output=False):
    inp, offset = parse()
    full_inp = inp * 10000
    part_inp = full_inp[offset:]

    for r in range(100):
        cs = [0] + list(accumulate(part_inp, operator.add))
        part_inp = [(cs[-1] - c) % 10 for c in cs]

    return ''.join(str(x) for x in part_inp[0:8])

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
