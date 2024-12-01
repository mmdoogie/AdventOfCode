with open('data/aoc_2015/20.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

tgt = int(dat[0])

def factors(n):
    fact = [i for i in range(1, int(n ** 0.5) + 1) if n % i == 0]
    return fact

def elves(house):
    f1 = set(factors(house))
    f2 = set(house // f for f in f1)
    return f1 | f2

def lazy_elves(house):
    e = elves(house)
    return [x for x in e if x * 50 >= house]

def presents(house):
    return 10 * sum(elves(house))

def lazy_presents(house):
    return 11 * sum(lazy_elves(house))

def part1(output = True):
    h = 1
    while True:
        p = presents(h)
        if p >= tgt:
            return h
        if output and h % 10000 == 0:
            print(h, p)
        h += 1
    return 0

def part2(output = True):
    h = 1
    while True:
        p = lazy_presents(h)
        if p >= tgt:
            return h
        if output and h % 10000 == 0:
            print(h, p)
        h += 1
    return 0

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
