from mrm.llist import llist

with open('data/aoc_2017/17.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    steps = int(dat[0])

def part1(output = True):
    del output

    buf = llist([0], circular = True)

    ins = 1
    at_el = buf.head()
    for _ in range(2017):
        at_el = at_el.far_right(steps)
        at_el = buf.insert_right_of(at_el, ins)
        ins += 1

    return at_el.right().val

def part2(output = True):
    ins = 1
    idx = 0
    beside = 0
    for _ in range(50000000):
        idx = (idx + steps) % ins
        if idx == 0:
            beside = ins
            if output:
                print(0, beside, '...')
        ins += 1
        idx += 1

    return beside

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
