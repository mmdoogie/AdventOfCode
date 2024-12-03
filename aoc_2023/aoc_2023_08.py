from itertools import cycle
from math import lcm

with open('data/aoc_2023/08.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    turns = dat[0]

    directions = {}
    for d in dat[2:]:
        node, dirs = d.split(' = ')
        dirs = dirs.split('(')[1].split(')')[0].split(', ')
        directions[node] = dirs

    return turns, directions

def part1(output = True):
    turns, directions = parse()

    curr_node = 'AAA'
    cnt = 0
    for t in cycle(turns):
        curr_node = directions[curr_node][0 if t == 'L' else 1]
        cnt += 1
        if curr_node == 'ZZZ':
            break

    return cnt

def part2(output = True):
    turns, directions = parse()

    start_nodes = [n for n in directions if n[2] == 'A']
    curr_nodes = [n for n in start_nodes]

    cycle1_counts = [0] * len(curr_nodes)
    cycle2_counts = [0] * len(curr_nodes)
    for t in cycle(turns):
        for i, node in enumerate(curr_nodes):
            if node[2] == 'Z':
                if output and cycle2_counts[i] == 0:
                    cycle2_counts[i] = cycle1_counts[i]
                    cycle1_counts[i] = 0
                else:
                    continue
            curr_nodes[i] = directions[node][0 if t == 'L' else 1]
            cycle1_counts[i] += 1
        if all(n[2] == 'Z' for n in curr_nodes):
            break

    if output:
        assert cycle1_counts == cycle2_counts
        for sn, en, cnt1, cnt2 in zip(start_nodes, curr_nodes, cycle1_counts, cycle2_counts):
            print(f'From {sn} to {en} requires {cnt1} steps (verified, 2nd cycle also takes {cnt2} steps)')

    all_steps = lcm(*cycle1_counts)
    if output:
        print(f'LCM of step counts: {all_steps}')
    return all_steps

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
