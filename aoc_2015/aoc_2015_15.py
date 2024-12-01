from mrm.util import product

with open('data/aoc_2015/15.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def get_ingrs():
    ingrs = {}
    for d in dat:
        p = d.split(': ')
        n = p[0]
        v = p[1].split(', ')
        params = [int(vv.split(' ')[1]) for vv in v]
        ingrs[n] = params
    return ingrs

def part1(output = True):
    ingrs = get_ingrs()

    maxval = 0
    for a in range(1, 100):
        for b in range(1, 100 - a):
            for c in range(1, 100 - a - b):
                d = 100 - a - b - c
                coeffs = (a, b, c, d)
                vals = [sum(n[x] * p for n, p in zip(ingrs.values(), coeffs)) for x in range(4)]
                if any(v < 0 for v in vals):
                    continue
                val = product(vals)
                if val > maxval:
                    if output:
                        print(f'{a:<3} {b:<3} {c:<3} {d:<3} --> {val}', vals)
                    maxval = val

    return maxval

def part2(output = True):
    ingrs = get_ingrs()

    maxval = 0
    for a in range(1, 100):
        for b in range(1, 100 - a):
            for c in range(1, 100 - a - b):
                d = 100 - a - b - c
                coeffs = (a, b, c, d)
                vals = [sum(n[x] * p for n, p in zip(ingrs.values(), coeffs)) for x in range(5)]
                if any(v < 0 for v in vals):
                    continue
                if vals[-1] != 500:
                    continue
                val = product(vals[:-1])
                if val > maxval:
                    if output:
                        print(f'{a:<3} {b:<3} {c:<3} {d:<3} --> {val}', vals)
                    maxval = val

    return maxval

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
