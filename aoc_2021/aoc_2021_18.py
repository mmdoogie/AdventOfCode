with open('data/aoc_2021/18.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def tolist(line):
    return [int(x) if x.isdigit() else x for x in list(line)]

def explode(line):
    depth = 0
    ni = {}
    left = False
    
    for i, c in enumerate(line):
        if c == '[':
            depth += 1
            left = True
        elif c == ']':
            depth -= 1
        elif c == ',':
            left = False
        else:
            ni[i] = (depth, left, c)
    
    nidx = sorted(list(ni.keys()))
    
    ll = [x for x in line]
    dl = -1
    for n, i in enumerate(nidx):
        (depth, left, c) = ni[i]
        if depth > 4:
            if left:
                if n > 0:
                    ll[nidx[n - 1]] = line[nidx[n - 1]] + line[i]
                dl = i - 1
            if not left:
                if n < len(nidx) - 1:
                    ll[nidx[n + 1]] = line[nidx[n + 1]] + line[i]
                ll[dl] = 0
                del(ll[dl+1:i+2])
                return (True, ll)

    return (False, line)

def allExplode(line):
    more = True
    did = False
    while more:
        (more, line) = explode(line)
        if more:
            did = True
    return (did, line)

def split(line):
    for i, c in enumerate(line):
        if c not in ['[',',',']'] and c >= 10:
            lv = int(c / 2)
            rv = int(c / 2 + 0.5)
            return (True, line[0:i] + ['[',lv,',',rv,']'] + line[i+1:])
    return (False, line)

def allSplit(line):
    more = True
    while more:
        (more, line) = split(line)
    return line

def add(line1, line2):
    return ['['] + line1 + [','] + line2 + [']']

def reduce(line):
    more = True
    while more:
        (more1, line) = allExplode(line)
        (more2, line) = split(line)
        more = more1 or more2
        
    return line

def mag(line):
    depth = 0
    ni = {}
    left = False
    
    for i, c in enumerate(line):
        if c == '[':
            depth += 1
            left = True
        elif c == ']':
            depth -= 1
        elif c == ',':
            left = False
        else:
            ni[i] = (depth, left, c)

    nidx = sorted(list(ni.keys()))

    ll = [x for x in line]
    dl = -1
    dlv = -1
    for n, i in enumerate(nidx):
        (depth, left, c) = ni[i]
        if left:
            dl = i - 1
            dlv = line[i]
        if not left:
            ll[dl] = 3*dlv+2*line[i]
            del(ll[dl+1:i+2])
            return (True, ll)

    return (False, line)

def allMag(line):
    more = True
    while more:
        (more, line) = mag(line)
        if len(line) == 1:
            return line[0]

def part1(output=False):
    val = tolist(dat[0])
    for v in dat[1:]:
        val = reduce(add(val, tolist(v)))

    allSum = ''.join([str(x) if type(x) is not str else x for x in val])
    sumMag = allMag(val)

    return allMag(val)

def part2(output=False):
    pairSums = {}
    for i, a in enumerate(dat):
        for j, b in enumerate(dat):
            if i == j:
                continue
            pairSums[(i,j)] = allMag(reduce(add(tolist(a),tolist(b))))

    maxSum = sorted(pairSums.items(), key=lambda x: x[1], reverse=True)[0][1]
    return maxSum
