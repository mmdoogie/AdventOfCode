from collections import deque

with open('data/aoc_2018/08.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def parse_node(vals):
    child_cnt = vals.popleft()
    meta_cnt = vals.popleft()

    children = {}
    for c in range(child_cnt):
        children[c + 1] = parse_node(vals)

    metadata = []
    for m in range(meta_cnt):
        metadata += [vals.popleft()]

    return {'children': children, 'metadata': metadata}

def sum_metadata(node):
    return sum(node['metadata']) + sum([sum_metadata(c) for c in node['children'].values()])

def node_value(node):
    if len(node['children']) == 0:
        return sum(node['metadata'])

    value = 0
    for m in node['metadata']:
        if m in node['children']:
            value += node_value(node['children'][m])
    return value

def part1(output = True):
    vals = deque([int(x) for x in dat[0].split(' ')])

    tree = parse_node(vals)
    assert len(vals) == 0

    return sum_metadata(tree)

def part2(output = True):
    vals = deque([int(x) for x in dat[0].split(' ')])

    tree = parse_node(vals)
    assert len(vals) == 0

    return node_value(tree)
