with open('data/aoc_2021/07.txt') as f:
    dat = [int(x) for x in f.readlines()[0].strip().split(",")]
minpos = min(dat)
maxpos = max(dat)

def part1(output=False):
    fuels = {p: sum([abs(d - p) for d in dat]) for p in range(minpos,maxpos+1)}
    minFuel = sorted(fuels.items(), key=lambda x: x[1])[0][1]
    return minFuel

def ns(x):
    return int(x*(x+1)/2)

def part2(output=False):
    expFuels = {p: sum([ns(abs(d - p)) for d in dat]) for p in range(minpos,maxpos+1)}
    minExpFuel = sorted(expFuels.items(), key=lambda x: x[1])[0][1]
    return minExpFuel
