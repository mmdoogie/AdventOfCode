def parse():
    with open('data/aoc_2022/05.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def printStacks(s):
    print([''.join(x) for x in s])


def part1(output=False):
    lines = parse()
    header = lines[0:8]
    moves = lines[10:]

    stacks = [[],[],[],[],[],[],[],[],[]]
    for l in header:
        for c in range(0, 9):
            x = l[1 + 4*c]
            if x != ' ':
                stacks[c] = [x] + stacks[c]

    for m in moves:
        parts = m.strip().split(" ")
        qty = int(parts[1])
        src = int(parts[3])-1
        dst = int(parts[5])-1

        if output:
            printStacks(stacks)
            print(m.strip())
        for n in range(qty):
            stacks[dst].append(stacks[src].pop())
        if output:
            printStacks(stacks)
            print()

    result = ''.join([s[-1] for s in stacks])
    return result

def part2(output=False):
    lines = parse()
    header = lines[0:8]
    moves = lines[10:]

    stacks = [[],[],[],[],[],[],[],[],[]]
    for l in header:
        for c in range(0, 9):
            x = l[1 + 4*c]
            if x != ' ':
                stacks[c] = [x] + stacks[c]

    for m in moves:
        parts = m.strip().split(" ")
        qty = int(parts[1])
        src = int(parts[3])-1
        dst = int(parts[5])-1

        if output:
            printStacks(stacks)
            print(m.strip())
        stacks[dst] = stacks[dst] + stacks[src][-qty:]
        stacks[src] = stacks[src][0:-qty]
        if output:
            printStacks(stacks)
            print()

    result = ''.join([s[-1] for s in stacks])
    return result
