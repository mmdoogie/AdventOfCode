from collections import defaultdict
import re

with open('data/aoc_2023/15.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def hash_alg(txt):
    val = 0
    for c in txt:
        val += ord(c)
        val *= 17
        val = val % 256
    return val

def part1(output = True):
    return sum(hash_alg(d) for d in dat[0].split(','))

def part2(output = True):
    boxes = defaultdict(lambda: [])
    focals = {}

    pattern = re.compile('([a-z]+)([-=])([1-9]?)')

    for d in dat[0].split(','):
        label, op, focal = pattern.match(d).groups()
        box = boxes[hash_alg(label)]
        if op == '-' and label in box:
            box.remove(label)
        elif op == '=':
            focals[label] = int(focal)
            if label not in box:
                box += [label]

    total_power = 0
    for box_num, lenses in boxes.items():
        if output and len(lenses) != 0:
            print()
            print('Box', box_num, 'contains:')
        for lens_num, lens_label in enumerate(lenses):
            lens_power = (1 + box_num) * (1 + lens_num) * focals[lens_label]
            total_power += lens_power
            if output:
                print(f'#{lens_num:<2d} {lens_label:8s} f={focals[lens_label]:<6d} power={lens_power:<6d} total={total_power:<6d}')

    return total_power

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
