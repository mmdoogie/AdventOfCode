import re
from collections import Counter

with open('data/aoc_2017/07.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    line_re = re.compile(r'([a-z]+) \(([0-9]+)\)( -> ([a-z, ]+))*')

    weight = {}
    children = {}
    parent = {}

    for d in dat:
        grps = line_re.match(d).groups()
        node = grps[0]
        weight[node] = int(grps[1])
        if grps[3]:
            child_list = [x.strip() for x in grps[3].split(',')]
            children[node] = child_list
            for c in child_list:
                parent[c] = node

def part1(output = True):
    del output

    lack_parent = set(weight.keys()) - set(parent.keys())

    assert len(lack_parent) == 1
    start_node = lack_parent.pop()

    return start_node

def accumulate(base_node):
    if base_node not in children:
        return weight[base_node]

    return weight[base_node] + sum(accumulate(c) for c in children[base_node])

def part2(output = True):
    start_node = part1(output)

    while True:
        tower_weights = [accumulate(x) for x in children[start_node]]
        weight_counter = Counter(tower_weights)

        if output:
            print('At Node:      ', start_node)
            print('Children:     ', children[start_node])
            print('Tower Weights:', tower_weights)
            print()

        if len(weight_counter) == 1:
            break

        bad_weight = weight_counter.most_common()[-1][0]
        bad_idx = tower_weights.index(bad_weight)
        start_node = children[start_node][bad_idx]

    tower_weights = [accumulate(x) for x in children[parent[start_node]]]
    weight_counter = Counter(tower_weights)
    weight_counts = weight_counter.most_common()
    good_weight = weight_counts[0][0]
    bad_weight = weight_counts[-1][0]
    corrected_weight = weight[start_node] - (bad_weight - good_weight)

    if output:
        print('Error Node:       ', start_node)
        print('Node Weight:      ', weight[start_node])
        print('Good Tree Weight: ', good_weight)
        print('Bad  Tree Weight: ', bad_weight)
        print('Corrected Weight: ', corrected_weight)
        print()

    return corrected_weight

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
