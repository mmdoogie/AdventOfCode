from itertools import permutations

with open('data/aoc_2017/02.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    rows = [[int(x) for x in l.split('\t')] for l in dat]

def part1(output = True):
    row_max = [max(x) for x in rows]
    row_min = [min(x) for x in rows]

    if output:
        for r, max_val, min_val in zip(rows, row_max, row_min):
            print(f'{str(r):99} MAX: {max_val:4}, MIN: {min_val:4}, CHK: {max_val - min_val:4}')

    val = sum(max_val - min_val for max_val, min_val in zip(row_max, row_min))
    return val

def part2(output = True):
    row_vals = [[(x, y) for x, y in permutations(r, 2) if x % y == 0] for r in rows]

    if output:
        for r, v in zip(rows, row_vals):
            assert len(v) == 1
            x, y = v[0]
            print(f'{str(r):99} {x:4} / {y:4} = {x // y:4}')

    return sum(x // y for r in row_vals for x, y in r)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
