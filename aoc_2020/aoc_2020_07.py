import re
from functools import cache

with open('data/aoc_2020/07.txt') as f:
    dat = [x.strip().strip('.') for x in f.readlines()]

bagmap = {}

@cache
def look_for_shiny_gold(basebag):
    if basebag not in bagmap:
        return False
    
    if 'shiny gold' in bagmap[basebag]:
        return True
    else:
        return any([look_for_shiny_gold(b) for b in bagmap[basebag]])

def part1(output=False):
    rh_re = re.compile(' [0-9]* ([a-z ]*) bag[s]{0,1}')
    for line in dat:
        lh, rh = line.split('contain')
        lh_bag = lh.split(' bags')[0]
        if rh[1] == 'n':
            rh_bags = []
        else:
            rh_bags = [rh_re.match(b).groups()[0] for b in rh.split(',')]
        bagmap[lh_bag] = rh_bags

    return sum([look_for_shiny_gold(b) for b in bagmap.keys()])

bagqty = {}

@cache
def contained_bags(basebag):
    if basebag not in bagqty:
        return 1

    return 1 + sum([contained_bags(k) * v for k, v in bagqty[basebag].items()])

def part2(output=False):
    rh_re = re.compile(' ([0-9]*) ([a-z ]*) bag[s]{0,1}')
    for line in dat:
        lh, rh = line.split('contain')
        lh_bag = lh.split(' bags')[0]
        if rh[1] == 'n':
            continue
        else:
            grps = [rh_re.match(b).groups() for b in rh.split(',')]
            rh_bags = {g[1]: int(g[0]) for g in grps}
        bagqty[lh_bag] = rh_bags

    return contained_bags('shiny gold') - 1
