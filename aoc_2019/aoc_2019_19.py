from aoc_2019.intcode import IntcodeComputer, PartialResult

def parse():
    with open('data/aoc_2019/19.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def check_pt(base_program, x, y):
    ic = IntcodeComputer(base_program)
    ic.input(x)
    ic.input(y)
    res = ic.run_partial()
    out = ic.output()
    return out

def part1(output = False):
    base_program = parse()
    pulled = 0
    for y in range(50):
        for x in range(50):
            out = check_pt(base_program, x, y)
            if output:
                if out == 1:
                    print('#', end='')
                else:
                    print(' ', end='')
            pulled += out
        if output:
            print()
    return pulled

def part2(output = False):
    base_program = parse()
    lhs = 0
    rhs = 0
    for x in range(1000):
        out = check_pt(base_program, x, 500)
        if out == 1 and lhs == 0:
            lhs = x
        if out == 1:
            rhs = x
        if rhs != 0 and out == 0:
            break

    u_slope = 500 / rhs
    l_slope = 500 / lhs

    x = (-99 - 99 * u_slope)/(u_slope - l_slope)
    y = l_slope * x

    rx = round(x)
    ry = round(y)
    
    if output:
        print('At y=500, x=', lhs, 'to', rhs)
        print('slopes', l_slope, u_slope)
        print('est', x, '->', rx, ',', y, '->', ry)

    while True:
        four_corn = [(rx, ry), (rx+99, ry), (rx, ry-99), (rx+99, ry-99)]
        corners_ok = sum([check_pt(base_program, *f) for f in four_corn])
        
        left_pts = [(x-1, y) for x,y in four_corn]
        move_left = sum([check_pt(base_program, *f) for f in left_pts])

        up_pts = [(x, y-1) for x,y in four_corn]
        move_up = sum([check_pt(base_program, *f) for f in up_pts])

        leftup_pts = [(x-1, y-1) for x, y in four_corn]
        move_leftup = sum([check_pt(base_program, *f) for f in leftup_pts])

        if output:
            print(rx, ry, corners_ok, move_left, move_up, move_leftup)

        if corners_ok == 4 and move_left < 4 and move_up < 4 and move_leftup < 4:
            return rx * 10000 + ry - 99

        if move_left == 4:
            rx -= 1
        elif move_up == 4:
            ry -= 1
        else:
            rx -= 1
            ry -= 1

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
