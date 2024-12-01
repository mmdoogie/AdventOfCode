with open('data/aoc_2015/25.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    locstr = dat[0].split('at row ')[1]
    row = int(locstr.split(',')[0])
    col = int(locstr.split('column ')[1].strip('.'))
    return row, col

def code(init):
    last = init
    yield last
    while True:
        nxt = last * 252533 % 33554393
        yield nxt
        last = nxt

def part1(output = True):
    row, col = parse()

    # Move to col in row 1
    r1c = col + row - 1
    # That's the top end of a diagonal with item number n(n+1)/2
    r1c_num = r1c * (r1c + 1) // 2
    # Then move back the same number of slots from the first op
    res_num = r1c_num - (row - 1)

    code_gen = code(20151125)
    for _ in range(res_num):
        res = next(code_gen)

    return res

def part2(output = True):
    return 'Start!'

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
