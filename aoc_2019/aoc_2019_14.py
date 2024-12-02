from collections import namedtuple
from functools import cache
from math import ceil

def parse():
    with open('data/aoc_2019/14.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    reactions = {}
    allchems = []
    for d in dat:
        lhs, rhs = d.split(' => ')

        rhs_split = rhs.split(' ')
        out_chem = rhs_split[1]
        out_qty = int(rhs_split[0])
        allchems += [out_chem]

        lhs_items = lhs.split(', ')
        in_items = []
        for l in lhs_items:
            l_split = l.split(' ')
            l_chem = l_split[1]
            l_qty = int(l_split[0])
            in_items += [(l_chem, l_qty)]
            allchems += [l_chem]

        reactions[out_chem] = (out_qty, in_items)

    return allchems, reactions

def produce(reactions, chem, min_qty, available):
    if chem in available and available[chem] >= min_qty:
        return 0

    r_prodqty, r_inps = reactions[chem]
    if chem in available:
        r_avail = available[chem]
    else:
        r_avail = 0
    
    r_reactqty = ceil((min_qty - r_avail) / r_prodqty)
    r_totalqty = r_reactqty * r_prodqty

    consumed_ore = 0
    for inp in r_inps:
        i_chem, i_qty = inp
        i_totalqty = i_qty * r_reactqty
        if i_chem == 'ORE':
            consumed_ore += i_totalqty
            continue

        consumed_ore += produce(reactions, i_chem, i_totalqty, available)
        available[i_chem] -= i_totalqty
    available[chem] += r_totalqty

    return consumed_ore

def part1(output=False):
    allchems, reactions = parse()
    available = {c: 0 for c in set(allchems)}
    ore = produce(reactions, 'FUEL', 1, available)
    return ore

def part2(output=False):
    allchems, reactions = parse()
    # Naive scale-up from producing 1 FUEL
    available = {c: 0 for c in set(allchems)}
    ore = produce(reactions, 'FUEL', 1, available)
    fuel = int(1e12) // ore

    # Now see how much that qty would require from scratch
    available = {c: 0 for c in set(allchems)}
    ore = produce(reactions, 'FUEL', fuel, available)

    # Scale that up and iterate a few times from there
    fuel = int(fuel * 1e12 / ore)
    available = {c: 0 for c in set(allchems)}
    ore = produce(reactions, 'FUEL', fuel, available)
    remain_ore = int(1e12) - ore

    i = 1
    while True:
        available = {c: 0 for c in set(allchems)}
        more_ore = produce(reactions, 'FUEL', fuel + i, available)
        if more_ore > remain_ore:
            break
        i += 1
    return fuel + i - 1

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
