with open('data/aoc_2021/02.txt') as f:
    dat = f.readlines()
    lines = [x.strip().split(' ') for x in dat]

def part1(output=False):
    x_cmds = [int(x[1]) for x in filter(lambda x: x[0] == 'forward', lines)]
    x_dist = sum(x_cmds)
    y_cmds = [int(x[1]) * (-1 if x[0] == 'up' else 1) for x in filter(lambda x: x[0] != 'forward', lines)]
    y_dist = sum(y_cmds)
    return x_dist * y_dist

def part2(output=False):
    x_pos = 0
    y_pos = 0
    aim = 0
    for c in lines:
        if c[0] == 'forward':
            x_pos += int(c[1])
            y_pos += int(c[1]) * aim
        elif c[0] == 'up':
            aim -= int(c[1])
        else:
            aim += int(c[1])
    return x_pos * y_pos
