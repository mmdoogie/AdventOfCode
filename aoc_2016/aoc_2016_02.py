import mrm.cpoint as pt

with open('data/aoc_2016/02.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    dirs = {'U': pt.UP, 'D': pt.DOWN, 'L': pt.LEFT, 'R': pt.RIGHT}

def get_code(btn_map):
    code = []
    at_pos = pt.ZERO
    for l in dat:
        for d in l:
            if at_pos + dirs[d] in btn_map:
                at_pos += dirs[d]
        code += [btn_map[at_pos]]
    return ''.join(code)

def part1(output = True):
    del output

    btns = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    locs = pt.adj_diag(pt.ZERO)
    btn_map = dict(zip(locs[:4] + [pt.ZERO] + locs[4:], btns))

    return get_code(btn_map)

def part2(output = True):
    del output

    btns = ['2', '3', '4', '6', '7', '8', 'A', 'B', 'C', '1', '5', '9', 'D']
    locs = pt.adj_diag(pt.ZERO) + [2*pt.UP, 2*pt.LEFT, 2*pt.RIGHT, 2*pt.DOWN]
    btn_map = dict(zip(locs[:4] + [pt.ZERO] + locs[4:], btns))

    return get_code(btn_map)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
