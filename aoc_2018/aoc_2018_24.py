from collections import namedtuple
from functools import partial
import re

from mrm.search import fn_binary_search

with open('data/aoc_2018/24.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

UNIT_HP_RE = re.compile(r'(\d+) units each with (\d+) hit points')
POWER_TYPE_INIT_RE = re.compile(r'attack that does (\d+) (\w+) damage at initiative (\d+)')

Group = namedtuple('Group', ['army', 'count', 'hp', 'power', 'type', 'initiative', 'immune', 'weak', 'desc'])

ARMIES = ['Immune', 'Infect']

def parse(boost = 0):
    groups = []
    army = ARMIES[0]
    unit_num = 0
    for d in dat:
        if ':' in d:
            continue

        if d == '':
            army = ARMIES[1]
            boost = 0
            unit_num = 0
            continue

        unit_num += 1

        uhp = [int(x) for x in UNIT_HP_RE.match(d).groups()]
        pti = [int(x) if i != 1 else x for i, x in enumerate(POWER_TYPE_INIT_RE.search(d).groups())]
        pti[0] += boost

        immune, weak = [], []
        if '(' in d:
            imm_weak = d.split('(')[1].split(')')[0].split('; ')
            for item in imm_weak:
                item_types = item.split(' to ')[1].split(', ')
                if item[0] == 'i':
                    immune = item_types
                else:
                    weak = item_types

        groups += [Group(army, *uhp, *pti, frozenset(immune), frozenset(weak), f'{army} {unit_num:02d}')]

    return groups

def effective_power(unit):
    return unit.count * unit.power

def max_damage(attacker, defender):
    if attacker.type in defender.immune:
        return 0

    raw_power = effective_power(attacker)

    if attacker.type in defender.weak:
        return 2 * raw_power

    return raw_power

def deal_damage(attacker, defender):
    raw_damage = max_damage(attacker, defender)

    units_killed = raw_damage // defender.hp

    if units_killed > defender.count:
        return None

    return defender._replace(count = defender.count - units_killed)

def target_priority(attacker, defender):
    return (max_damage(attacker, defender), effective_power(defender), defender.initiative)

def play_game(boost = 0, output = False):
    armies = parse(boost)

    it = 0
    while True:
        it += 1

        # Target Phase
        targets = {}
        priority = sorted(armies, key = lambda x: (effective_power(x), x.initiative), reverse = True)
        for attacker in priority:
            dmg = [(target_priority(attacker, defender), defender) for defender in priority if attacker.army != defender.army and defender not in targets.values()]
            if sum(d[0][0] for d in dmg) == 0:
                continue
            targets[attacker] = max(dmg)[1]
        if output:
            print()
            print('Round', it)
            print('--Target Phase--')
            print('Selection Priority:', ', '.join(p.desc for p in priority))
            print('Targets Selected:  ', ', '.join(targets[p].desc if p in targets else 'None     ' for p in priority))

        # Attack Phase
        priority = sorted(armies, key = lambda x: x.initiative, reverse = True)
        if output:
            print('--Attack Phase--')
            print('Attack Priority:   ', ', '.join(p.desc if p in targets else 'None     ' for p in priority))
            print('Result:             ', end='')
        killed = []
        replaced = {}
        for attacker in priority:
            if attacker in killed or attacker not in targets:
                if output:
                    print('-skip-   , ', end='')
                continue
            target = targets[attacker]
            attacker = replaced.get(attacker, attacker)
            target = replaced.get(target, target)
            result = deal_damage(attacker, target)
            if result is None:
                killed += [target]
            else:
                replaced[target] = result
            if output:
                print('-elim-   ' if result is None else f'{target.count - result.count:<4d} kill, ', end='')

        new_armies = []
        for a in armies:
            if a in replaced:
                new_armies += [replaced[a]]
            elif a not in killed:
                new_armies += [a]

        units = [sum(a.count for a in new_armies if a.army == t) for t in ARMIES]
        if output:
            print()
            print(f'After round: {ARMIES[0]} has {units[0]} and {ARMIES[1]} has {units[1]} units')
        if armies == new_armies or any(u == 0 for u in units):
            return units

        armies = new_armies

def part1(output = True):
    units = play_game(boost = 0, output = output)
    return max(units)

def part2(output = True):
    _, _, _, rr = fn_binary_search(partial(play_game, output = False), 1, lambda x: x[1] == 0, max_find_multiple = 10, output = output)
    return rr[0]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
