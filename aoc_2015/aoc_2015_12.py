import json

with open('data/aoc_2015/12.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
jj = json.loads(dat[0])

def traverse(node, filt_red):
    total = 0
    if isinstance(node, list):
        for item in node:
            total += traverse(item, filt_red)
        return total
    if isinstance(node, dict):
        if not filt_red or "red" not in node.values():
            for v in node.values():
                total += traverse(v, filt_red)
        return total
    if isinstance(node, int):
        return node
    if isinstance(node, str):
        return 0
    print('error', type(node), node)
    return 0

def part1(output = True):
    a = traverse(jj, False)
    return a

def part2(output = True):
    a = traverse(jj, True)
    return a

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
