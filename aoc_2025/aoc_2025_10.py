import re

import z3

from mrm.dijkstra import Dictlike, dijkstra
from mrm.parse import all_nums

def parse():
    with open('data/aoc_2025/10.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    line_pat = re.compile(r'\[([.#]+)\] ((?:\([0-9,]+\)\s)+){([0-9,]+)}')
    vals = []
    for l in lines:
        lp, bp, jv = line_pat.match(l).groups()
        lp = tuple(c == '#' for c in lp)
        bp = [tuple(all_nums(b)) for b in bp.split(' ') if b]
        jv = tuple(all_nums(jv))
        vals += [(lp, bp, jv)]
    return vals

def part1(output=False):
    lines = parse()

    tot = 0
    for l in lines:
        light_pattern, button_patterns, _ = l
        start_pattern = tuple([False] * len(light_pattern))

        def ngh(pat):
            cand = []
            for bp in button_patterns:
                cand += [tuple(p ^ (i in bp) for i, p in enumerate(pat))]
            return cand

        wts = dijkstra(Dictlike(ngh), start_point=start_pattern, end_point=light_pattern, keep_paths=False)
        tot += wts[light_pattern]

    return tot

def part2(output=False):
    lines = parse()

    tot = 0
    for l in lines:
        _, button_patterns, joltage = l

        solver = z3.Optimize()
        coeffs = [z3.Int(f'x{i}') for i in range(len(button_patterns))]
        for c in coeffs:
            solver.add(c >= 0)

        for ji, jv in enumerate(joltage):
            used = []
            for i, btns in enumerate(button_patterns):
                if ji in btns:
                    used += [coeffs[i]]
            solver.add(sum(used) == jv)
        solver.minimize(sum(coeffs))
        assert solver.check() == z3.sat
        pushes = solver.model().evaluate(sum(coeffs)).as_long()
        tot += pushes

    return tot

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
