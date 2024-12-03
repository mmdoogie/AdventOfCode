from functools import reduce

with open('data/aoc_2021/16.txt') as f:
    dat = f.readlines()[0].strip()

def hex2bin(hs):
    bs = ''
    for h in hs:
        bs += format(int(h, 16), '04b')
    return bs

bindat = hex2bin(dat)

def parsePacket(b, i):
    v = int(b[i+0:i+3], 2)
    t = int(b[i+3:i+6], 2)
    i = i + 6
    
    if t == 4:
        ds = ''
        while True:
            more = b[i] == '1'
            ds += b[i+1:i+5]
            i += 5
            if not more:
                break
        d = int(ds, 2)
        return (i, (v, t, d))
    else:
        if b[i] == '0': #15 bits total length
            i += 1
            end = i + 15 + int(b[i:i+15], 2)
            i += 15
            subpkts = []
            while i < end:
                i, pkt = parsePacket(b, i)
                subpkts += [pkt]
            d = subpkts
        else: #11 bit subpacket count
            i += 1
            cnt = int(b[i:i+11], 2)
            i += 11
            subpkts = []
            for f in range(cnt):
                i, pkt = parsePacket(b, i)
                subpkts += [pkt]
            d = subpkts
        return (i, (v, t, d))
    return 0

def verSum(pkt):
    vs = pkt[0]
    if pkt[1] != 4:
        for p in pkt[2]:
            vs += verSum(p)
    return vs

def part1(output=False):
    pkts = parsePacket(bindat, 0)[1]
    vs = verSum(pkts)
    return vs


def evalPacket(pkt):
    if pkt[1] == 4:
        return pkt[2]

    vals = [evalPacket(p) for p in pkt[2]]

    if pkt[1] == 0:
        return sum(vals)
    elif pkt[1] == 1:
        return reduce(lambda a, b: a * b, vals)
    elif pkt[1] == 2:
        return min(vals)
    elif pkt[1] == 3:
        return max(vals)
    elif pkt[1] == 5:
        return 1 if vals[0] > vals[1] else 0
    elif pkt[1] == 6:
        return 1 if vals[0] < vals[1] else 0
    elif pkt[1] == 7:
        return 1 if vals[0] == vals[1] else 0

def part2(output=False):
    pkts = parsePacket(bindat, 0)[1]
    return evalPacket(pkts)
