from copy import copy
with open('data/aoc_2021/03.txt') as f:
    dat = [x.strip() for x in f.readlines()]
width = len(dat[0])

def part1(output=False):
    transp = [[int(x[i]) for x in dat] for i in range(width)]
    sums = [sum(x) for x in transp]
    mcv = ['1' if x > len(dat)/2 else '0' for x in sums]
    gamma_val = int(''.join(mcv), 2)
    epsilon_val = 2**width-1-gamma_val
    return gamma_val * epsilon_val

def part2(output=False):
    max_vals = copy(dat)
    min_vals = copy(dat)

    for p in range(width):
        max_pv = [int(x[p]) for x in max_vals]
        min_pv = [int(x[p]) for x in min_vals]

        mcv = '1' if sum(max_pv) >= len(max_vals)/2 else '0'
        lcv = '1' if sum(min_pv) <  len(min_vals)/2 else '0'

        max_vals = list(filter(lambda x: x[p] == mcv, max_vals))    
        if len(max_vals) == 1:
            ogr_val = max_vals[0]

        min_vals = list(filter(lambda x: x[p] == lcv, min_vals))
        if len(min_vals) == 1:
            co2_val = min_vals[0]

    return int(ogr_val, 2) * int(co2_val, 2)
