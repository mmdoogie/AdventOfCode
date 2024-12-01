import operator

with open('data/aoc_2015/21.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

boss = {}
for d in dat:
    k, v = d.split(': ')
    boss[k] = int(v)
boss_vals = tuple(boss.values())

weapons = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
armor = [(13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
rings = [(25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]

def wins(wep, ac):
    hp = 100
    bhp = boss_vals[0]

    while True:
        dmg = max(1, wep - boss_vals[2])
        bhp -= dmg
        if bhp <= 0:
            return True

        dmg = max(1, boss_vals[1] - ac)
        hp -= dmg
        if hp <= 0:
            return False
    return False

def try_all_combos(cond = True, cmp_fn = operator.lt, cost_def = 1000):
    opt_cost = cost_def

    for w in weapons:
        cost = w[0]
        dmg = w[1]
        ac = 0
        if wins(dmg, ac) == cond and cmp_fn(cost, opt_cost):
            opt_cost = cost

        for a in armor:
            cost = w[0] + a[0]
            ac = a[2]
            if wins(dmg, ac) == cond and cmp_fn(cost, opt_cost):
                opt_cost = cost

            for r1 in rings:
                cost = w[0] + a[0] + r1[0]
                dmg = w[1] + r1[1]
                ac = a[2] + r1[2]
                if wins(dmg, ac) == cond and cmp_fn(cost, opt_cost):
                    opt_cost = cost

                for r2 in rings:
                    if r1 == r2:
                        continue
                    cost = w[0] + a[0] + r1[0] + r2[0]
                    dmg = w[1] + r1[1] + r2[1]
                    ac = a[2] + r1[2] + r2[2]
                    if wins(dmg, ac) == cond and cmp_fn(cost, opt_cost):
                        opt_cost = cost

    return opt_cost

def part1(output = True):
    return try_all_combos(cond = True, cmp_fn = operator.lt, cost_def = 1000)

def part2(output = True):
    return try_all_combos(cond = False, cmp_fn = operator.gt, cost_def = 0)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
