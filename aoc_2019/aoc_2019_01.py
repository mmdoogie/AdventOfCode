def parse():
    with open('data/aoc_2019/01.txt') as f:
        dat = [x.strip() for x in f.readlines()]
    fuels = [int(m) // 3 - 2 for m in dat]
    return fuels

def part1(output=False):
    fuels = parse()
    totalFuel = sum(fuels)
    return totalFuel

def part2(output=False):
    fuels = parse()
    totalFuel = sum(fuels)
    for f in fuels:
        addFuel = f // 3 - 2
        while addFuel > 0:
            totalFuel += addFuel
            addFuel = addFuel // 3 - 2
    return totalFuel

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
