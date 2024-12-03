with open('data/aoc_2021/06.txt') as f:
    dat = f.readlines()[0].strip()

def part1(output=False):
    fish = [int(f) for f in dat.split(",")]
    for d in range(80):
        fish = [f-1 for f in fish]
        spawn = [1 if f == -1 else 0 for f in fish]
        fish = [f+7*s for f,s in zip(fish, spawn)] + [8]*sum(spawn)

    return len(fish)

def part2(output=False):
    fish = [int(f) for f in dat.split(",")]
    cnts = dict()
    for c in range(9):
        cnts[c] = len([f for f in fish if f == c])

    for d in range(256):
        for c in range(9):
            cnts[c-1] = cnts[c]
        cnts[8] = cnts[-1]
        cnts[6] += cnts[-1]
        cnts[-1] = 0

    return sum(cnts.values())
