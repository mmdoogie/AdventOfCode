with open('data/aoc_2018/13.txt') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def find_trains():
    trains = {}
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            if c == '^' or c == 'v' or c == '<' or c == '>':
                trains[(x, y)] = (c, 0)
    return trains

def move_trains(eliminate_crashes = False, output = True):
    grid = [list(d) for d in dat]

    trains = find_trains()
    dir_steps = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
    left_turn  = {'^': '<', 'v': '>', '<': 'v', '>': '^'}
    right_turn = {'^': '>', 'v': '<', '<': '^', '>': 'v'}

    ticks = 0
    while True:
        ticks += 1
        new_trains = {}
        crash_skip = []
        order = sorted(trains.keys(), key = lambda x: 1000 * x[1] + x[0])
        
        for o in order:
            if o in crash_skip:
                continue
            x, y = o
            direction, turns = trains[o]
            sx, sy = dir_steps[direction]
            c = grid[y+sy][x+sx]
            match c:
                case '-' | '|':
                    nti = (direction, turns)
                case '\\':
                    if sx == -1:
                        nti = ('^', turns)
                    elif sx == 1:
                        nti = ('v', turns)
                    elif sy == -1:
                        nti = ('<', turns)
                    elif sy == 1:
                        nti = ('>', turns)
                case '/':
                    if sx == -1:
                        nti = ('v', turns)
                    elif sx == 1:
                        nti = ('^', turns)
                    elif sy == -1:
                        nti = ('>', turns)
                    elif sy == 1:
                        nti = ('<', turns)
                case '+':
                    if turns == 0:
                        nti = (left_turn[direction], (turns + 1) % 3)
                    elif turns == 1:
                        nti = (direction, (turns + 1) % 3)
                    elif turns == 2:
                        nti = (right_turn[direction], (turns + 1) % 3)
                case '^' | 'v' | '<' | '>':
                    nti = (direction, turns)
                case _:
                    assert False
            ntl = (x + sx, y + sy)
            if (ntl in trains and order.index(ntl) > order.index(o)) or ntl in new_trains:
                if output:
                    print('Crash detected at', ntl, 'in tick', ticks)
                if not eliminate_crashes:
                    return ','.join([str(v) for v in ntl])
                else:
                    crash_skip += [ntl]
                    if ntl in new_trains:
                        del new_trains[ntl]
            else:
                new_trains[ntl] = nti
        if output and len(trains) != len(new_trains):
            print('Remaining trains', len(new_trains), 'after tick', ticks)
        trains = new_trains
        if len(trains.keys()) == 1:
            return ','.join([str(v) for v in list(trains.keys())[0]])

    return 0

def part1(output = True):
    return move_trains(eliminate_crashes = False, output = output)

def part2(output = True):
    return move_trains(eliminate_crashes = True, output = output)
