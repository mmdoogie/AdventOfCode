with open('data/aoc_2018/05.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def collapse(polymer, output = True):
    pairs = [chr(x) + chr(x + ord('A') - ord('a')) for x in range(ord('a'), ord('z') + 1)]
    pairs += [chr(x + ord('A') - ord('a')) + chr(x) for x in range(ord('a'), ord('z') + 1)]

    if output:
        print(polymer)
    while True:
        changed = False
        for p in pairs:
            if p in polymer:
                changed = True
                loc = polymer.index(p)
                polymer = polymer[:loc] + polymer[loc+2:]
                if output:
                    print('Found', p, 'at', loc)
        if not changed:
            break

    if output:
        print('Final', polymer)

    return polymer

def part1(output = True):
    polymer = collapse(dat[0], output)
    return len(polymer)

def part2(output = True):
    polymer = collapse(dat[0], False)

    unit_types = set(polymer.upper())
    final_lens = {}
    for u in unit_types:
        reduced_polymer = polymer.replace(u, '').replace(u.lower(), '')
        final_lens[u] = len(collapse(reduced_polymer, False))
        if output:
            print('Removing unit', u, 'reduces to', final_lens[u])

    return min(final_lens.values())
