with open('data/aoc_2017/09.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def process(output = True):
    stream = list(dat[0])

    if output:
        print('Initial length:        ', len(stream))

    cancel = set()
    for i, ch in enumerate(stream):
        if i in cancel:
            continue
        if ch == '!':
            cancel.add(i)
            cancel.add(i + 1)

    stream = [x for i, x in enumerate(stream) if i not in cancel]

    if output:
        print('Phase 1 - Cancellation:', len(stream))

    garbage = set()
    garbage_count = 0
    start_garb = 0
    for i, ch in enumerate(stream):
        if ch == '<' and start_garb == 0:
            start_garb = i
        if ch == '>':
            assert start_garb != 0
            garbage.update(range(start_garb, i + 1))
            garbage_count += 1
            start_garb = 0

    stream = [x for i, x in enumerate(stream) if i not in garbage]
    ucg_rem = len(garbage) - 2 * garbage_count

    if output:
        print('Phase 2 - Degarbaging: ', len(stream))
        print('Noncancelled Garbage:  ', ucg_rem)
        print('Final groups:', ''.join(stream))

    depth = 0
    score = 0
    for ch in stream:
        if ch == '{':
            depth += 1
            score += depth
        elif ch == '}':
            depth -= 1
        elif ch == ',':
            continue
        else:
            assert False

    return score, ucg_rem

def part1(output = True):
    score, _ = process(output)
    return score

def part2(output = True):
    _, ucg_rem = process(output)
    return ucg_rem

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
