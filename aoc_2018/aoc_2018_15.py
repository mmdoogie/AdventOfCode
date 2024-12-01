from functools import total_ordering

import mrm.ansi_term as ansi
from mrm.dijkstra import dijkstra

with open('data/aoc_2018/15.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

@total_ordering
class Unit():
    def __init__(self, x, y, kind, ap = 3, hp = 200):
        self._hc = f'{kind}@{x},{y}'
        self.x = x
        self.y = y
        self.kind = kind
        self.ap = ap
        self.hp = hp

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False
        return self._hc == other._hc

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def __repr__(self):
        return self.kind + '@' + str(self.x) + ',' + str(self.y) + '[' + str(self.hp) + ']'

    def __hash__(self):
        return hash(self._hc)

def parse_dat(elf_power = 3):
    spaces = {}
    units = set()
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            if c == '#':
                continue
            spaces[(x, y)] = True
            if c == 'E':
                units.add(Unit(x, y, c, ap = elf_power))
            elif c == 'G':
                units.add(Unit(x, y, c))
    return units, spaces

def move_order(units, already_moved):
    return sorted(list(units.difference(already_moved)))

def adj_targets(unit, umap):
    x, y = unit.x, unit.y
    adj = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    tgt = [uu for uu in [umap[a] for a in adj if a in umap] if uu.kind != unit.kind]
    return sorted(tgt, key = lambda x: (x.hp, x.y, x.x))

def make_adj(unit, umap, spaces):
    adj = {}
    for s in spaces.keys():
        if (unit.x != s[0] or unit.y != s[1]) and s in umap:
            adj[s] = []
        else:
            x, y = s
            ngh_pos = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            adj[s] = sorted([n for n in ngh_pos if n in spaces], key = lambda x: (x[1], x[0]))
    return adj

def viz(weights, unit, umap, spaces, path = [], elf_power = 3):
    ansi.cursor_home()

    min_x = min(k[0] for k in spaces.keys())
    max_x = max(k[0] for k in spaces.keys())
    min_y = min(k[1] for k in spaces.keys())
    max_y = max(k[1] for k in spaces.keys())
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) in umap:
                uu = umap[(x, y)]
            else:
                uu = False
            if unit.x == x and unit.y == y:
                if unit.kind == 'E':
                    print(ansi.green('EE '), end='')
                else:
                    print(ansi.red('GG '), end='')
            elif (x, y) in weights and uu:
                if uu.kind == 'E':
                    print(ansi.green(f'{weights[(x, y)]:02d} '), end='')
                else:
                    print(ansi.red(f'{weights[(x, y)]:02d} '), end='')
            elif uu:
                print(ansi.yellow(f'U{uu.kind} '), end='')
            elif (x, y) in path:
                print(ansi.blue(f'{path.index((x, y)):02d} '), end='')
            elif (x, y) in spaces:
                print('__ ', end='')
            else:
                print('   ', end='')
        print()
    print('Elves:', sum(u.kind == 'E' for u in umap.values()), end=', ')
    print('Gnomes:', sum(u.kind == 'G' for u in umap.values()), ansi.CLEAR_LINE)
    print('Elf Power:', elf_power)

def closest(weights, unit, umap):
    act_weights = [(v, k[1], k[0]) for k, v in weights.items() if k in umap and umap[k].kind != unit.kind]
    order = sorted(act_weights)
    if len(order) == 0:
        return None
    return (order[0][2], order[0][1])

def play_game(output = True, elf_power = 3, end_at_first_loss = False):
    units, spaces = parse_dat(elf_power = elf_power)
    umap = {(u.x, u.y): u for u in units}
    start_elves = sum(u.kind == 'E' for u in units)

    rounds_complete = 0
    already_moved = set()
    while True:
        order = move_order(units, already_moved)
        o = order[0]
        if sum(u.kind != o.kind for u in units) == 0:
            if output:
                print('winner found in round:', rounds_complete + 1)
            break
        targets = adj_targets(o, umap)
        if len(targets) == 0:
            ngh = make_adj(o, umap, spaces)
            weights, paths = dijkstra(ngh, start_point=(o.x, o.y))
            move_tgt = closest(weights, o, umap)
            if move_tgt is not None:
                move_path = paths[move_tgt]
                if output:
                    viz(weights, o, umap, spaces, move_path, elf_power)
                del umap[(o.x, o.y)]
                o.x = move_path[1][0]
                o.y = move_path[1][1]
                umap[(o.x, o.y)] = o
            else:
                if output:
                    viz(weights, o, umap, spaces, elf_power = elf_power)
        already_moved.add(o)
        targets = adj_targets(o, umap)
        if len(targets) != 0:
            if output:
                viz(weights, o, umap, spaces, elf_power = elf_power)
            targets[0].hp -= o.ap
            if targets[0].hp <= 0:
                if targets[0].kind == 'E' and end_at_first_loss:
                    return 0, 1
                units.remove(targets[0])
                del umap[(targets[0].x, targets[0].y)]
                if targets[0] in already_moved:
                    already_moved.remove(targets[0])

        if len(already_moved) == len(units):
            rounds_complete += 1
            if output:
                viz(set(), o, umap, spaces, elf_power = elf_power)
                print('rounds  complete:', rounds_complete)
            already_moved = set()

    final_elves = sum(u.kind == 'E' for u in units)
    return rounds_complete * sum(u.hp for u in units), start_elves - final_elves

def part1(output = True):
    if output:
        ansi.clear_screen()
        with ansi.hidden_cursor():
            score, _ = play_game(True)
    else:
        score, _ = play_game(False)
    return score

def part2(output = True):
    elf_power = 4
    while True:
        if output:
            ansi.clear_screen()
            with ansi.hidden_cursor():
                score, elves_lost = play_game(True, elf_power = elf_power, end_at_first_loss = True)
        else:
            score, elves_lost = play_game(False, elf_power = elf_power, end_at_first_loss = True)
        if elves_lost == 0:
            return score
        elf_power += 1

if __name__ == '__main__':
    print('Part 1:', part1(False))
    #print('Part 2:', part2(True))
