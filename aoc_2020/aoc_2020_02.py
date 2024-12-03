with open('data/aoc_2020/02.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output=False):
    valid = 0
    for line in dat:
        items = line.split(' ')
        pol = [int(x) for x in items[0].split('-')]
        ltr = items[1].split(':')[0]
        pwd = items[2]

        match = sum([1 if a == ltr else 0 for a in list(pwd)])

        if match >= pol[0] and match <= pol[1]:
            valid += 1

    return valid

def part2(output=False):
    valid = 0
    for line in dat:
        items = line.split(' ')
        pol = [int(x) for x in items[0].split('-')]
        ltr = items[1].split(':')[0]
        pwd = items[2]

        match = sum([1 if pwd[a - 1] == ltr else 0 for a in pol])

        if match == 1:
            valid += 1

    return valid
