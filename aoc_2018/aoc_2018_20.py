from collections import deque, defaultdict

import mrm.ansi_term as ansi
from mrm.dijkstra import dijkstra

with open('data/aoc_2018/20.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    depths = deque()
    parens = {}

    for i, c in enumerate(dat[0]):
        if c in '(^':
            depths.append(i)
        elif c in ')$':
            left  = depths.pop()
            parens[left] = i

    assert len(depths) == 0
    return parens

def expand(parens, left):
    right = parens[left]

    opset = []
    group = []
    skipuntil = -1

    txt = ''
    for i, c in enumerate(dat[0][left + 1:right + 1]):
        if i < skipuntil:
            continue

        if c in 'NSEW':
            txt += c
        elif txt != '':
            group += [txt]
            txt = ''

        if c == '(':
            group += [expand(parens, left + i + 1)]
            skipuntil = parens[left + i + 1] - left
        elif c in '|)':
            opset += [group]
            group = []

    if txt != '':
        group += [txt]
    if group != []:
        opset += [group]

    return opset

DIR_MOVES = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

def print_explored(adj, bx, by):
    pts = adj.keys()

    ansi.cursor_home()

    for y in range(by - 25, by + 25):
        for x in range(bx - 75, bx + 75):
            if (x, y) in pts:
                if x == bx and y == by:
                    print(ansi.yellow('#'), end = '')
                else:
                    print('#', end = '')
            else:
                print(' ', end = '')
        print()

def explore(opset, adj, base_point, output):
    bx, by = base_point

    for o in opset:
        if isinstance(o, list):
            explore(o, adj, (bx, by), output)
        else:
            assert isinstance(o, str)
            for c in o:
                dx = bx + DIR_MOVES[c][0]
                dy = by + DIR_MOVES[c][1]
                adj[(bx, by)] += [(dx, dy)]
                adj[(dx, dy)] += [(bx, by)]
                bx, by = dx, dy
                if output:
                    print_explored(adj, bx, by)
                    print(o, ansi.CLEAR_LINE)

room_weights = None

def part1(output = True):
    global room_weights

    parens = parse()
    opset = expand(parens, 0)
    adj = defaultdict(lambda: [])
    if output:
        ansi.clear_screen()
        with ansi.hidden_cursor():
            explore(opset, adj, (0, 0), True)
    else:
        explore(opset, adj, (0, 0), False)
    room_weights = dijkstra(adj, start_point = (0, 0), keep_paths = False)
    furthest_door = max(w for w in room_weights.values())
    return furthest_door

def print_by_weights(weights):
    pts = weights.keys()

    ansi.cursor_home()

    for y in range(-50, 50):
        for x in range(-75, 75):
            if (x, y) in pts:
                dist = weights[(x, y)]
                if dist == 0:
                    print('o', end = '')
                elif dist < 100:
                    print(ansi.red('#'), end = '')
                elif dist < 500:
                    print(ansi.yellow('#'), end = '')
                elif dist < 1000:
                    print(ansi.green('#'), end = '')
                else:
                    print(ansi.blue('#'), end = '')
            else:
                print(' ', end = '')
        print()

    print(' ' * 50, 'Red: <100 / Yellow: <500 / Green: <1000 / Blue: >=1000')

def part2(output = True):
    if room_weights is None:
        part1(False)
    if output:
        ansi.clear_screen()
        with ansi.hidden_cursor():
            print_by_weights(room_weights)
    return sum(w >= 1000 for w in room_weights.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
