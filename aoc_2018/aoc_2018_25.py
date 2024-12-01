from functools import cache

with open('data/aoc_2018/25.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

@cache
def manhat(a, b):
    return sum(abs(b[i] - a[i]) for i in range(4))

def part1(output = True):
    points = [tuple(int(x) for x in d.split(',')) for d in dat]

    remain = set(points)
    con_count = 1
    con = [remain.pop()]

    while len(remain) > 0:
        remove = set()
        for r in remain:
            if any(manhat(r, cp) <= 3 for cp in con):
                remove.add(r)
                con += [r]
        remain = remain.difference(remove)

        if len(remove) == 0:
            con_count += 1
            con = [remain.pop()]

        if output:
            print(f'Constellations: {con_count:>3d}, Remaining points: {len(remain):>4d}')

    return con_count

def part2(output = True):
    return 'Underflow!'

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
