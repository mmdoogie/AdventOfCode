with open('data/aoc_2021/08.txt') as f:
    dat = f.readlines()

io = [d.strip().split("|") for d in dat]
ostr = [x[1].strip().split(" ") for x in io]
osort = [[''.join(sorted(v)) for v in x] for x in ostr]

def part1(output=False):
    olen = [len(v) for x in ostr for v in x]
    care = [2, 3, 4, 7]
    these = sum([1 if l in care else 0 for l in olen])
    return these

def str_in(a, b):
    return len(set(a) - set(b)) == 0

def deduce(s):
    res = dict()
    ires = dict()

    easy = {2: 1, 4: 4, 3: 7, 7: 8}
    lens = [len(x) for x in s]

    for i, l in enumerate(lens):
        if l in easy:
            res[s[i]] = easy[l]
            ires[easy[l]] = s[i]

    if 1 in ires:
        for x in s:
            if x in res:
                continue
            if len(x) == 5 and str_in(ires[1], x):
                res[x] = 3
                ires[3] = x
            if len(x) == 6 and not str_in(ires[1], x):
                res[x] = 6
                ires[6] = x

    if 4 in ires:
        for x in s:
            if x in res:
                continue
            if len(x) == 6 and str_in(ires[4], x):
                res[x] = 9
                ires[9] = x
            if len(x) == 6 and not str_in(ires[4], x) and 6 in ires:
                res[x] = 0
                ires[0] = x

    if 1 in ires and 4 in ires:
        part = ''.join(set(ires[4]) - set(ires[1]))
        for x in s:
            if x in res:
                continue
            if len(x) == 5 and str_in(part, x):
                res[x] = 5
                ires[5] = x
            if len(x) == 5 and not str_in(part, x) and 3 in ires:
                res[x] = 2
                ires[2] = x

    nums = [res[x] if x in res else x for x in s]
    return int(''.join([str(x) for x in nums[-4:]]))

def part2(output=False):
    istr = [x[0].strip().split(" ") for x in io]
    isort = [[''.join(sorted(v)) for v in x] for x in istr]
    iosort = [i + o for i, o in zip(isort,osort)]
    out = sum([deduce(x) for x in iosort])
    return out
