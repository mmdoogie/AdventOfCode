def parse():
    with open('data/aoc_2022/06.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines[0]

def findMarker(signal, markerLen):
    for n in range(len(signal)):
        chars = signal[n:n+markerLen]
        if len(set(chars)) == markerLen:
            return n+markerLen

def part1(output=False):
    signal = parse()
    return findMarker(signal, 4)

def part2(output=False):
    signal = parse()
    return findMarker(signal, 14)
