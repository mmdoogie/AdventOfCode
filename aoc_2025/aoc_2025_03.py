def parse():
    with open('data/aoc_2025/03.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    vals = [[int(x) for x in l] for l in lines]
    return vals

def get_val(arr):
    return int(''.join(str(a) for a in arr))

def part1(output=False):
    lines = parse()

    tot = 0
    for l in lines:
        poss = [(l[i], max(l[i+1:])) for i in range(len(l) - 1)]
        max_val = max(poss)
        tot += get_val(max_val)

    return tot

def part2(output=False):
    lines = parse()

    tot = 0
    for l in lines:
        curr_set = l[-12:]
        for r in reversed(l[:-12]):
            try_vals = []
            for p in range(12):
                next_set = [r] + curr_set[:p] + curr_set[p+1:]
                try_vals += [next_set]
            curr_set = max(curr_set, *try_vals)
        tot += get_val(curr_set)
    return tot

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
