from itertools import combinations
from sympy import solve, symbols

with open('data/aoc_2023/24.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    stones = []
    for d in dat:
        pos, vel = d.split(' @ ')
        pos = [int(p) for p in pos.split(', ')]
        vel = [int(v) for v in vel.split(', ')]
        stones += [pos + vel]
    return stones

def part1(output = True):
    stones = parse()

    cnt = 0
    for a, b in combinations(stones, 2):
        m_a = a[4]/a[3]
        y_a = a[1]
        x_a = a[0]
        b_a = y_a-m_a*x_a

        m_b = b[4]/b[3]
        y_b = b[1]
        x_b = b[0]
        b_b = y_b-m_b*x_b

        if m_a == m_b:
            continue

        ix = (b_b-b_a)/(m_a-m_b)
        iy = m_a*ix+b_a

        if (ix-x_a)/a[3] < 0 or (ix-x_b)/b[3] < 0:
            continue

        if 200000000000000 <= ix <= 400000000000000 and 200000000000000 <= iy <= 400000000000000:
            cnt += 1

    return cnt

def part2(output = True):
    stones = parse()

    x_0, y_0, z_0 = symbols('x_0, y_0, z_0')
    v_x, v_y, v_z = symbols('v_x, v_y, v_z')
    t_1, t_2, t_3 = symbols('t_:3')
    all_vars = [x_0, y_0, z_0, v_x, v_y, v_z, t_1, t_2, t_3]

    eqns = [ x_0 + v_x * t_1 - stones[0][0] - stones[0][3] * t_1,
             y_0 + v_y * t_1 - stones[0][1] - stones[0][4] * t_1,
             z_0 + v_z * t_1 - stones[0][2] - stones[0][5] * t_1,
             x_0 + v_x * t_2 - stones[1][0] - stones[1][3] * t_2,
             y_0 + v_y * t_2 - stones[1][1] - stones[1][4] * t_2,
             z_0 + v_z * t_2 - stones[1][2] - stones[1][5] * t_2,
             x_0 + v_x * t_3 - stones[2][0] - stones[2][3] * t_3,
             y_0 + v_y * t_3 - stones[2][1] - stones[2][4] * t_3,
             z_0 + v_z * t_3 - stones[2][2] - stones[2][5] * t_3 ]

    sols = list(solve(eqns, all_vars, dict=True))
    assert len(sols) == 1
    sol = sols[0]

    return int(sol[x_0] + sol[y_0] + sol[z_0])

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
