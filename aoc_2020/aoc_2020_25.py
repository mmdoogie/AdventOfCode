with open('data/aoc_2020/25.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def transform(subject, loopsize):
    n = 1
    for l in range(loopsize):
        n = (n * subject) % 20201227
    return n

def part1(output=False):
    pk1 = int(dat[0])
    pk2 = int(dat[1])

    ls1 = 0
    ls2 = 0
    n = 1
    i = 0
    while True:
        n = (n * 7) % 20201227
        i += 1
        if n == pk1:
            ls1 = i
        if n == pk2:
            ls2 = i
        if ls1 > 0 and ls2 > 0:
            break

    n = 1
    for l in range(ls1):
        n = (n * pk2) % 20201227

    return n

def part2(output=False):
    return 'Check!'
