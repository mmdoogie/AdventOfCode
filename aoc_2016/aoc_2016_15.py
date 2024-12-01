from mrm.crt import crt

with open('data/aoc_2016/15.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    discs = [(int(d.split(' ')[3]), int(d[-2])) for d in dat]

def part1(output = True):
    del output

    mods = [d[0] for d in discs]
    offsets = [d[1] for d in discs]
    desires = list(range(-1, -len(mods) - 1, -1))
    vals = [(d - o) % m for d, o, m in zip(desires, offsets, mods)]

    return crt(vals, mods)

def part2(output = True):
    del output

    mods = [d[0] for d in discs] + [11]
    offsets = [d[1] for d in discs] + [0]
    desires = list(range(-1, -len(mods) - 1, -1))
    vals = [(d - o) % m for d, o, m in zip(desires, offsets, mods)]

    return crt(vals, mods)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
#Disc #1 has 7 positions; at time=0, it is at position 0.
