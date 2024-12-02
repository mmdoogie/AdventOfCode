from collections import namedtuple
from itertools import combinations
from math import gcd

def parse():
    with open('data/aoc_2019/12.txt') as f:
        dat = [x.strip() for x in f.readlines()]
    moons = ['io', 'europa', 'ganymede', 'callisto']
    initial_positions = [Pt3(*[int(x.split('=')[1]) for x in d.strip('>').split(', ')]) for d in dat]
    return moons, initial_positions

Pt3 = namedtuple('Pt3', ['x', 'y', 'z'])

def part1(output=False):
    moons, initial_positions = parse()
    position = {moons[i]: initial_positions[i] for i in range(len(initial_positions))}
    velocity = {moons[i]: Pt3(0, 0, 0) for i in range(len(initial_positions))}

    for it in range(1000):
        for m1, m2 in combinations(moons, 2):
            if position[m1].x > position[m2].x:
                vd_x = 1
            elif position[m1].x < position[m2].x:
                vd_x = -1
            else:
                vd_x = 0

            if position[m1].y > position[m2].y:
                vd_y = 1
            elif position[m1].y < position[m2].y:
                vd_y = -1
            else:
                vd_y = 0

            if position[m1].z > position[m2].z:
                vd_z = 1
            elif position[m1].z < position[m2].z:
                vd_z = -1
            else:
                vd_z = 0

            velocity[m1] = Pt3(velocity[m1].x - vd_x, velocity[m1].y - vd_y, velocity[m1].z - vd_z)
            velocity[m2] = Pt3(velocity[m2].x + vd_x, velocity[m2].y + vd_y, velocity[m2].z + vd_z)

        for m in moons:
            position[m] = Pt3(position[m].x + velocity[m].x, position[m].y + velocity[m].y, position[m].z + velocity[m].z)

    pot_eng = [abs(position[m].x) + abs(position[m].y) + abs(position[m].z) for m in moons]
    kin_eng = [abs(velocity[m].x) + abs(velocity[m].y) + abs(velocity[m].z) for m in moons]
    tot_eng = sum([a * b for a, b in zip(pot_eng, kin_eng)])

    return tot_eng


def part2(output=False):
    moons, initial_positions = parse()
    position = {moons[i]: initial_positions[i] for i in range(len(initial_positions))}
    match_pos = dict(position)
    velocity = {moons[i]: Pt3(0, 0, 0) for i in range(len(initial_positions))}

    found_cycle = Pt3(False, False, False)
    i = 0

    while not all(found_cycle):
        for m1, m2 in combinations(moons, 2):
            if position[m1].x > position[m2].x:
                vd_x = 1
            elif position[m1].x < position[m2].x:
                vd_x = -1
            else:
                vd_x = 0

            if position[m1].y > position[m2].y:
                vd_y = 1
            elif position[m1].y < position[m2].y:
                vd_y = -1
            else:
                vd_y = 0

            if position[m1].z > position[m2].z:
                vd_z = 1
            elif position[m1].z < position[m2].z:
                vd_z = -1
            else:
                vd_z = 0

            velocity[m1] = Pt3(velocity[m1].x - vd_x, velocity[m1].y - vd_y, velocity[m1].z - vd_z)
            velocity[m2] = Pt3(velocity[m2].x + vd_x, velocity[m2].y + vd_y, velocity[m2].z + vd_z)

        for m in moons:
            position[m] = Pt3(position[m].x + velocity[m].x, position[m].y + velocity[m].y, position[m].z + velocity[m].z)

        i += 1

        if not found_cycle.x and all([position[m].x == match_pos[m].x and velocity[m].x == 0 for m in moons]):
            found_cycle = found_cycle._replace(x=i)
        if not found_cycle.y and all([position[m].y == match_pos[m].y and velocity[m].y == 0 for m in moons]):
            found_cycle = found_cycle._replace(y=i)
        if not found_cycle.z and all([position[m].z == match_pos[m].z and velocity[m].z == 0 for m in moons]):
            found_cycle = found_cycle._replace(z=i)

    xy_cycle = found_cycle.x * found_cycle.y // gcd(found_cycle.x, found_cycle.y)
    xyz_cycle = found_cycle.z * xy_cycle // gcd(found_cycle.z, xy_cycle)

    return xyz_cycle

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
