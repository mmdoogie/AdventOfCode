with open('data/aoc_2020/16.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def compute():
    ranges = {}
    tickets = []
    validTickets = []
    myTicket = None

    rangeMode = True
    ticketMode = False
    for d in dat:
        if d == '':
            continue
        if d.startswith('your'):
            rangeMode = False
            ticketMode = False
            continue
        if d.startswith('nearby'):
            ticketMode = True
            continue
        if rangeMode:
            name, vals = d.split(': ')
            ranges[name] = [[int(x) for x in r.split('-')] for r in vals.split(' or ')]
        elif ticketMode:
            tickets += [[int(x) for x in d.split(',')]]
        else:
            myTicket = [int(x) for x in d.split(',')]

    invSum = 0
    for t in tickets:
        rej = False
        for n in t:
            found = False
            for r in ranges.values():
                if (n >= r[0][0] and n <= r[0][1]) or (n >= r[1][0] and n <= r[1][1]):
                    found = True
                    break
            if not found:
                invSum += n
                rej = True
        if not rej:
            validTickets += [t]

    validTickets += [myTicket]

    rangeIndex = {}
    for n, r in ranges.items():
        cands = []
        for i in range(len(validTickets[0])):
            vals = [t[i] for t in validTickets]
            if all([(v >= r[0][0] and v <= r[0][1]) or (v >= r[1][0] and v <= r[1][1]) for v in vals]):
                cands += [i]
        rangeIndex[n] = cands

    finalRange = {}
    while len(finalRange) < len(ranges):
        remove = None
        for n, r in rangeIndex.items():
            if len(r) == 1 and n not in finalRange:
                finalRange[n] = r[0]
                remove = r[0]
                break
        if remove is not None:
            for n in rangeIndex.keys():
                if remove in rangeIndex[n]:
                    rangeIndex[n].remove(remove)

    myDep = 1
    for n, i in finalRange.items():
        if n.startswith('departure'):
            myDep *= myTicket[i]

    return invSum, myDep

def part1(output=False):
    invSum, _ = compute()
    return invSum

def part2(output=False):
    _, myDep = compute()
    return myDep
