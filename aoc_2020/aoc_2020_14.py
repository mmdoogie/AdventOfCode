with open('data/aoc_2020/14.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output=False):
    mem = {}
    andMask = 0
    orMask = 0

    for d in dat:
        op, val = d.split(' = ')

        if op == 'mask':
            orMask = int(val.replace('X', '0'), 2)
            andMask = int(val.replace('X', '1'), 2)
        else:
            addr = int(op.split('[')[1].split(']')[0])
            newVal = (int(val) | orMask) & andMask
            mem[addr] = newVal

    return sum(mem.values())

def part2(output=False):
    mem = {}
    andMask = 0
    orMask = 0

    for d in dat:

        op, val = d.split(' = ')

        if op == 'mask':
            orMask = int(val.replace('X', '0'), 2)
            xLocs = [i for i, c in enumerate(val) if c == 'X']

        else:
            baseAddr = format(int(op.split('[')[1].split(']')[0]) | orMask, "036b")
            for n in range(2**len(xLocs)):
                bits = format(n, f'0{len(xLocs)}b')
                addr = list(baseAddr)
                for i, xi in enumerate(xLocs):
                    addr[xi] = bits[i]
                addr = ''.join(addr)
                mem[addr] = int(val)

    return sum(mem.values())
