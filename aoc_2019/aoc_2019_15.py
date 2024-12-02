from collections import deque
from aoc_2019.intcode import IntcodeComputer, PartialResult
from mrm.dijkstra import dijkstra

def parse():
    with open('data/aoc_2019/15.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def point_for_dir(x, y, d):
    if d == 1:
        return (x, y - 1)
    elif d == 2:
        return (x, y + 1)
    elif d == 3:
        return (x - 1, y)
    elif d == 4:
        return (x + 1, y)

def return_dir(d):
    if d == 1:
        return 2
    elif d == 2:
        return 1
    elif d == 3:
        return 4
    elif d == 4:
        return 3

def explore(ic, state, x, y, d):
    ic.input(d)
    ic.run_partial()
    res = ic.output()

    rpt = point_for_dir(x, y, d)
    state[rpt] = res

    if res != 0:
        for xd in range(1, 5):
            if point_for_dir(*rpt, xd) not in state:
                explore(ic, state, *rpt, xd)

        ic.input(return_dir(d))
        ic.run_partial()
        res = ic.output()
        assert res != 0

def prepare():
    base_program = parse()
    ic = IntcodeComputer(base_program)

    state = {}
    explore(ic, state, 0, 0, 1)
    explore(ic, state, 0, 0, 2)
    explore(ic, state, 0, 0, 3)
    explore(ic, state, 0, 0, 4)

    oxy = [k for k, v in state.items() if v == 2][0]
    spaces = [k for k, v in state.items() if v != 0]
    neighbors = {}
    for sp in spaces:
        ngh_cand = [point_for_dir(*sp, d) for d in range(1, 5)]
        ngh = [n for n in ngh_cand if n in spaces]
        neighbors[sp] = ngh
    return neighbors, oxy

def part1(output=False):
    neighbors, oxy = prepare()
    weights = dijkstra(neighbors, start_point=(0, 0), end_point=oxy, keep_paths=False)
    return weights[oxy]

def part2(output=False):
    neighbors, oxy = prepare()
    weights = dijkstra(neighbors, start_point=oxy, keep_paths=False)
    return max(weights.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
