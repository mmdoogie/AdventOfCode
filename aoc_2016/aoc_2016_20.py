with open('data/aoc_2016/20.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    blacklist = []
    for d in dat:
        a, b = d.split('-')
        blacklist += [(int(a), int(b))]

def part1(output = True):
    start = 0
    end = 0
    for a, b in sorted(blacklist):
        if a > end:
            if output:
                print(f'Disjoint found! Range ({a}, {b}) leaves gap of {a - end - 1}')
            if a - end - 1 >= 1:
                return end + 1
        if b > end:
            end = b
        if output:
            print(f'Range ({a}, {b}) part of block covering ({start}, {end}).')

    return 0

def part2(output = True):
    end = 0
    allowed = 0
    for a, b in sorted(blacklist):
        if a > end:
            gap = a - end - 1
            allowed += gap
            if output and gap:
                print(f'Gap between {end:10} and {a:10} admits {gap}, total allowed {allowed}')
            end = b
            continue
        if b > end:
            end = b

    return allowed

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
