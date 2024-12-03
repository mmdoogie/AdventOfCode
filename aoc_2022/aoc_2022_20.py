def parse(k=1):
    with open('data/aoc_2022/20.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    order  = [(k * int(l), n) for n, l in enumerate(lines)]
    result = [(k * int(l), n) for n, l in enumerate(lines)]
    count  = len(order)
    return order, result, count

def part1(output=False):
    order, result, count = parse()

    for o in order:
        src = result.index(o)
        dst = (src + o[0]) % (count - 1)
        if dst == 0:
            dst = count-1
        elif dst == count-1:
            dst = 0
        result.pop(src)
        result.insert(dst, o[0])

    idx0 = result.index(0)
    idx1k = (idx0 + 1000) % count
    idx2k = (idx0 + 2000) % count
    idx3k = (idx0 + 3000) % count
    if output:
        print(idx0, idx1k, idx2k, idx3k, sum([result[idx1k], result[idx2k], result[idx3k]]))

    return sum([result[idx1k], result[idx2k], result[idx3k]])

def part2(output=False):
    k = 811589153
    order, result, count = parse(k)

    for t in range(10):
        for o in order:
            src = result.index(o)
            dst = (src + o[0]) % (count - 1)
            if dst == 0:
                dst = count-1
            elif dst == count-1:
                dst = 0
            result.pop(src)
            result.insert(dst, o)

    result = [r[0] for r in result]

    idx0 = result.index(0)
    idx1k = (idx0 + 1000) % count
    idx2k = (idx0 + 2000) % count
    idx3k = (idx0 + 3000) % count
    if output:
        print(idx0, idx1k, idx2k, idx3k, sum([result[idx1k], result[idx2k], result[idx3k]]))

    return sum([result[idx1k], result[idx2k], result[idx3k]])
