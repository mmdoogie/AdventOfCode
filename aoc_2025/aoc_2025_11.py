from mrm.cache import Keycache

def parse():
    with open('data/aoc_2025/11.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    ngh = {}
    for l in lines:
        frm, to_list = l.split(': ')
        ngh[frm] = to_list.split(' ')

    return ngh

def part1(output=False):
    ngh = parse()
    start_pt = 'you'

    @Keycache(stats=True)
    def dfs(frm, *, key):
        if frm == 'out':
            return 1
        return sum(dfs(n, key=n) for n in ngh[frm])

    paths = dfs(start_pt, key=start_pt)
    if output:
        hit, miss = dfs.stats()
        print(f'Cache Stats: {hit} hits, {miss} misses. {hit / (hit + miss) * 100:.2f}% hit ratio.')

    return paths

def part2(output=False):
    ngh = parse()
    start_pt = 'svr'

    @Keycache(stats=True)
    def dfs(frm, cs, *, key):
        if frm == 'out':
            return cs == 11
        if frm == 'dac' and cs < 10:
            cs += 10
        if frm == 'fft' and not cs % 1:
            cs += 1
        return sum(dfs(n, cs, key=(n, cs)) for n in ngh[frm])

    paths = dfs(start_pt, 0, key=(start_pt, 0))
    if output:
        hit, miss = dfs.stats()
        print(f'Cache Stats: {hit} hits, {miss} misses. {hit / (hit + miss) * 100:.2f}% hit ratio.')

    return paths

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
