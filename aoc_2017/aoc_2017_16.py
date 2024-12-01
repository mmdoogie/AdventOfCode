with open('data/aoc_2017/16.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    moves = dat[0].split(',')

def part1(output = True, override_progs = None):
    progs = [chr(ord('a') + x) for x in range(16)]
    if override_progs:
        progs = override_progs

    for m in moves:
        if m[0] == 's':
            sz = int(m[1:])
            progs = progs[-sz:] + progs[:-sz]
        if m[0] == 'x':
            vals = [int(x) for x in m[1:].split('/')]
            p1 = progs[vals[0]]
            p2 = progs[vals[1]]
            progs[vals[0]] = p2
            progs[vals[1]] = p1
        if m[0] == 'p':
            idx1 = progs.index(m[1])
            idx2 = progs.index(m[3])
            progs[idx1] = m[3]
            progs[idx2] = m[1]
        if output:
            print(f'{m:10}', ''.join(progs))

    return ''.join(progs)

def part2(output = True):
    progs = [chr(ord('a') + x) for x in range(16)]

    next_dance = ''.join(progs)
    seen = {next_dance: 0}
    if output:
        print(0, next_dance)

    i = 1
    while True:
        next_dance = part1(False, list(next_dance))
        if output:
            print(i, next_dance)
        if next_dance in seen:
            break
        seen[next_dance] = i
        i += 1

    step = 1000000000 % i
    idx = list(seen.values()).index(step)
    cfg = list(seen.keys())[idx]

    if output:
        print(f'{next_dance} repeated from {seen[next_dance]} at dance {i}')
        print(f'1000000000 % {i} = {idx} -> {cfg}')

    return cfg

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
