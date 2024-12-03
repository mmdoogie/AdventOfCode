with open('data/aoc_2021/01.txt') as f:
    dat = [int(x) for x in f.readlines()]

def part1(output=False):
    diff = [x[1] - x[0] for x in zip([0] + dat, dat + [0])]
    total = len(list(filter(lambda x: x > 0, diff)))
    return total - 1

def part2(output=False):
    wind = [sum(dat[x:x+3]) for x in range(0, len(dat)-2)]
    wind_diff = [x[1] - x[0] for x in zip([0] + wind, wind + [0])]
    wind_total = len(list(filter(lambda x: x > 0, wind_diff)))
    return wind_total - 1
