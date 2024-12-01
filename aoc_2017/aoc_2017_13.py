with open('data/aoc_2017/13.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    layers = {}
    for d in dat:
        l, r = d.split(': ', 2)
        layers[int(l)] = int(r)

def part1(output = True):
    scanners = {l: 0 for l in layers}
    scan_dir = {l: 1 for l in layers}
    caught = []

    for ps in range(max(layers.keys()) + 1):
        if ps in scanners and scanners[ps] == 0:
            caught += [ps]
        for s in scanners:
            scanners[s] += scan_dir[s]
            if scan_dir[s] == 1 and scanners[s] == layers[s]-1:
                scan_dir[s] = -1
            elif scan_dir[s] == -1 and scanners[s] == 0:
                scan_dir[s] = 1

    if output:
        print('Caught in layers', caught)

    severity = sum(c * layers[c] for c in caught)
    return severity

def part2(output = True):
    delay = 0

    while True:
        caught = False

        for ps, rng in layers.items():
            if (delay + ps) % (2 * rng - 2) == 0:
                caught = True
                break

        if output and caught and delay % 100000 == 0:
            print('Delay', delay, 'Caught in layer', ps)

        if not caught:
            return delay

        delay += 1

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
