from collections import defaultdict

with open('data/aoc_2016/10.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def run_bots(to_outputs):
    bots = defaultdict(list)
    bins = defaultdict(list)

    rules = {}

    for d in dat:
        bits = d.split(' ')
        if 'goes' in d:
            val = int(bits[1])
            bot = int(bits[5])
            bots[bot] += [val]
        else:
            bot = int(bits[1])
            low_type = bots if bits[5] == 'bot' else bins
            low_loc = int(bits[6])
            high_type = bots if bits[10] == 'bot' else bins
            high_loc = int(bits[11])
            rules[bot] = [low_type[low_loc], high_type[high_loc]]

    while True:
        ready = [b for b in bots if len(bots[b]) == 2]
        b = ready.pop()
        for dst, val in zip(rules[b], sorted(bots[b])):
            dst += [val]

        if not to_outputs and 61 in bots[b] and 17 in bots[b]:
            return b

        bots[b] = []

        if to_outputs and bins[0] and bins[1] and bins[2]:
            return bins[0][0] * bins[1][0] * bins[2][0]

    return 0

def part1(output = True):
    del output
    return run_bots(False)

def part2(output = True):
    del output
    return run_bots(True)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
