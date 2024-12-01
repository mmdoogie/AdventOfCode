from dataclasses import dataclass, field
from heapq import heappush, heappop

with open('data/aoc_2015/22.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

boss_dat = {}
for d in dat:
    k, v = d.split(': ')
    boss_dat[k] = int(v)

@dataclass(frozen=True)
class Spell:
    name:   str
    cost:   int
    dmg:    int = 0
    heal:   int = 0
    dot:    int = 0
    armor:  int = 0
    poison: int = 0
    manaup: int = 0

spells = [
    Spell('MM', cost=53,  dmg=4),
    Spell('Dr', cost=73,  dmg=2, heal=2),
    Spell('Sh', cost=113, dot=6, armor=7),
    Spell('Po', cost=173, dot=6, poison=3),
    Spell('Re', cost=229, dot=5, manaup=101),
]

@dataclass(frozen=True, order=True)
class State:
    player_hp:   int   = field(compare=False)
    boss_hp:     int   = field(compare=False)
    player_mana: int   = field(compare=False)
    mana_total:  int
    spell_dot:   tuple = field(compare=False)
    hard_mode:   bool  = field(compare=False)

def valid_next_states(cs):
    nss = set()
    for i, cast in enumerate(spells):
        ac = 0
        php = cs.player_hp
        bhp = cs.boss_hp
        mana = cs.player_mana
        cost = cs.mana_total
        dots = cs.spell_dot

        if dots[i] > 1:
            continue

        if cs.hard_mode:
            php -= 1
            if php <= 0:
                continue
        for sp, tr in zip(spells, dots):
            if not tr:
                continue
            if sp.armor:
                ac = sp.armor
            bhp -= sp.poison
            mana += sp.manaup
        dots = [max(0, d - 1) for d in dots]

        if cast.cost > mana:
            continue

        if bhp <= 0:
            nss.add(State(php, bhp, mana, cost, tuple(dots), cs.hard_mode))
            continue

        mana -= cast.cost
        cost += cast.cost
        bhp -= cast.dmg
        php += cast.heal
        if cast.dot:
            dots[i] = cast.dot
        if bhp <= 0:
            nss.add(State(php, bhp, mana, cost, tuple(dots), cs.hard_mode))
            continue

        ac = 0
        for sp, tr in zip(spells, dots):
            if not tr:
                continue
            if sp.armor:
                ac = sp.armor
            bhp -= sp.poison
            mana += sp.manaup
        dots = [max(0, d - 1) for d in dots]
        if bhp <= 0:
            nss.add(State(php, bhp, mana, cost, tuple(dots), cs.hard_mode))
            continue

        dmg = max(1, boss_dat['Damage'] - ac)
        php -= dmg
        if php <= 0:
            continue

        nss.add(State(php, bhp, mana, cost, tuple(dots), cs.hard_mode))

    return nss

def search(fs):
    hq = [fs]
    min_total = 1000000
    while hq:
        cs = heappop(hq)
        ns = valid_next_states(cs)
        for n in ns:
            if n.boss_hp <= 0:
                min_total = min(min_total, n.mana_total)
                continue
            if n.mana_total < min_total:
                heappush(hq, n)
    return min_total

def part1(output = True):
    return search(State(50, boss_dat['Hit Points'], 500, 0, tuple(0 for s in spells), False))

def part2(output = True):
    return search(State(50, boss_dat['Hit Points'], 500, 0, tuple(0 for s in spells), True))

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
