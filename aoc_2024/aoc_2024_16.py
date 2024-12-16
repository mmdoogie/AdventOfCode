from functools import partial

import mrm.cpoint as cpt
from mrm.dijkstra import Dictlike, dijkstra

def parse():
    with open('data/aoc_2024/16.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid, inv = cpt.grid_as_dict(lines, valid=lambda x: x in '.SE', with_inv=True)
    return grid, inv

def ngh_fun(grid, state):
    pos, head = state
    ngh = []
    if pos + head in grid:
        ngh += [(pos + head, head)]
    ngh += [(pos, cpt.left_turn(head)), (pos, cpt.right_turn(head))]
    return ngh

@Dictlike
def wt(edge):
    state1, state2 = edge
    if state1[1] == state2[1]:
        return 1
    return 1000

def part1(output=False):
    grid, inv = parse()

    start_state = (inv['S'].pop(), cpt.RIGHT)
    end_point = inv['E'].pop()
    end_states = [(end_point, h) for h in cpt.HEADINGS]
    ngh = Dictlike(partial(ngh_fun, grid))

    w = dijkstra(ngh, wt, start_state, end_states, keep_paths=False)

    return min(v for k, v in w.items() if k[0] == end_point)

def part2(output=False):
    grid, inv = parse()

    start_state = (inv['S'].pop(), cpt.RIGHT)
    end_point = inv['E'].pop()
    ngh = Dictlike(partial(ngh_fun, grid))

    w_start = dijkstra(ngh, wt, start_state, keep_paths=False)

    min_path = min((v, k) for k, v in w_start.items() if k[0] == end_point)

    w_end = dijkstra(ngh, wt, (min_path[1][0], cpt.u_turn(min_path[1][1])), keep_paths=False)

    min_set = set()
    for sk, sv in w_start.items():
        ek = (sk[0], cpt.u_turn(sk[1]))
        if sv + w_end[ek] == min_path[0]:
            min_set.add(sk[0])
    return len(min_set)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
