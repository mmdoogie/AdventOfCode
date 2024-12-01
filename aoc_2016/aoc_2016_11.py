from collections import defaultdict
from itertools import combinations
import re

from mrm.dijkstra import dijkstra

with open('data/aoc_2016/11.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    item_re = re.compile(r'a ([a-z]+)( generator|-compatible microchip)')
    gen_floors = {}
    chip_floors = {}
    elements = set()
    for floor, d in enumerate(dat):
        floor_items = item_re.findall(d)
        for elem, item in floor_items:
            elements.add(elem)
            if 'generator' in item:
                gen_floors[elem] = floor
            else:
                chip_floors[elem] = floor

def state_valid(state, el_cnt):
    gens = state[:el_cnt]
    chips = state[el_cnt:2*el_cnt]
    for g, c in zip(gens, chips):
        if g != c and c in gens:
            return False
    return True

def gen_graph(initial_state):
    to_make = set([initial_state])
    edges = defaultdict(list)
    el_cnt = (len(initial_state) - 1) // 2
    tmp1 = list(combinations(list(range(2*el_cnt)),1))
    tmp2 = list(combinations(list(range(2*el_cnt)),2))
    while to_make:
        state = to_make.pop()
        if state[-1] > 0:
            f = state[-1] - 1
            for t in tmp1:
                if state[t[0]] != state[-1]:
                    continue
                new_state = list(state)
                new_state[t[0]] = f
                new_state[-1] = f
                if state_valid(new_state, el_cnt):
                    ns = tuple(new_state)
                    edges[state] += [ns]
                    if ns not in edges:
                        to_make.add(ns)
        if state[-1] < 3:
            f = state[-1] + 1
            for t in tmp2:
                if state[t[0]] != state[-1] or state[t[1]] != state[-1]:
                    continue
                new_state = list(state)
                new_state[t[0]] = f
                new_state[t[1]] = f
                new_state[-1] = f
                if state_valid(new_state, el_cnt):
                    ns = tuple(new_state)
                    edges[state] += [ns]
                    if ns not in edges:
                        to_make.add(ns)
    return edges

def part1(output = True):
    del output
    ini = tuple([gen_floors[e] for e in elements] + [chip_floors[e] for e in elements] + [0])
    fin = tuple([3 for _ in ini])
    edg = gen_graph(ini)
    w = dijkstra(edg, start_point=ini, end_point=fin, keep_paths = False)
    return w[fin]

def part2(output = True):
    ini = tuple([gen_floors[e] for e in elements] + [0, 0] + [chip_floors[e] for e in elements] + [0, 0, 0])
    fin = tuple([3 for _ in ini])
    edg = gen_graph(ini)
    w = dijkstra(edg, start_point=ini, end_point=fin, keep_paths = False)
    return w[fin]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
