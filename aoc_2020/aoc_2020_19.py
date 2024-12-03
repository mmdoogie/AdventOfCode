import itertools

with open('data/aoc_2020/19.txt') as f:
    dat = [x.strip() for x in f.readlines()]

rules = {}
for d in dat:
    if ':' not in d:
        break
    num, pat = d.split(': ')
    if 'a' in pat or 'b' in pat:
        rules[int(num)] = [pat[1]]
    else:
        if '|' in pat:
            rules[int(num)] = [[int(x) for x in y.split(' ')] for y in pat.split(' | ')]
        else:
            rules[int(num)] = [[int(x) for x in pat.split(' ')]]

def matchrule(txt, rn):
    if txt == '':
        return (False, None)

    rp = rules[rn]

    if rp[0] == 'a' or rp[0] == 'b':
        if txt[0] == rp[0]:
            return (True, txt[1:])
        else:
            return (False, None)
    else:
        for rs in rp:
            mr = txt
            for r in rs:
                ms, mr = matchrule(mr, r)
                if not ms:
                    break
            if ms:
                return (True, mr)
        return (False, None)

def part1(output=False):
    validMsgs = 0
    for d in dat:
        if ':' in d or d == '':
            continue
        ms, mr = matchrule(d, 0)
        if ms and mr == '':
            validMsgs += 1
    return validMsgs

def part2(output=False):
    validMsgs = 0
    for d in dat:
        if ':' in d or d == '':
            continue
        found = False
        for x8, x11 in itertools.product(range(1,6), repeat=2):
            rules[8] = [[42]*x8]
            rules[11] = [[42]*x11 + [31]*x11]

            ms, mr = matchrule(d, 0)
            if ms and mr == '':
                found = True
                break
        if found:
            validMsgs += 1
            continue

    return validMsgs 
