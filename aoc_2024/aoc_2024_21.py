from collections import Counter
from itertools import pairwise
import string

import mrm.cpoint as cpt
from mrm.graph import bfs_min_paths
from mrm.util import repeatedly_apply

def parse():
    with open('data/aoc_2024/21.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

char_map = {cpt.UP: '^', cpt.DOWN: 'v', cpt.LEFT: '<', cpt.RIGHT: '>', 0: 'A'}
inv_char = {v: k for k, v in char_map.items()}

def path_to_moves(path):
    moves = ''
    for a, b in pairwise(path):
        moves += char_map[b - a]
    moves += 'A'

    return moves

def condense(cnt, pat):
    res = ''
    for p in pat:
        if p in cnt:
            res += p * cnt[p]
    return res

def kp_to_arrow(seq):
    kp = ['789', '456', '123', 'x0A']
    kp_grid = cpt.grid_as_dict(kp, lambda x: x != 'x')
    kp_inv = {v: k for k, v in kp_grid.items()}
    kp_ngh = {k: cpt.adj_ortho(k, kp_grid) for k in kp_grid}

    path = []
    for frm, to in pairwise('A' + seq):
        p = bfs_min_paths(kp_ngh, kp_inv[frm])
        path += p[kp_inv[to]][0]

    moves = path_to_moves(path)

    def kpsort(path):
        atpt = kp_inv['A']
        res = []
        for sp in path.split('A'):
            cnt = Counter(sp)
            if (atpt == kp_inv['A'] and '<' in cnt and cnt['<'] > 1) or (atpt == kp_inv['0'] and '<' in cnt):
                pat = '^<'
            elif 'v' in cnt and '>' in cnt and ((atpt == kp_inv['7'] and cnt['v'] == 3) or (atpt == kp_inv['4'] and cnt['v'] == 2) or atpt == kp_inv['1']):
                pat = '>v'
            else:
                pat = '<v^>'
            res += [condense(cnt, pat)]
            atpt += sum(inv_char[x] for x in sp)
        return 'A'.join(res)

    return kpsort(moves)

def arrow_to_arrow(seq):
    kp = ['x^A', '<v>']
    kp_grid = cpt.grid_as_dict(kp, lambda x: x != 'x')
    kp_inv = {v: k for k, v in kp_grid.items()}
    kp_ngh = {k: cpt.adj_ortho(k, kp_grid) for k in kp_grid}

    def unsorted_path(frm, to):
        p = bfs_min_paths(kp_ngh, kp_inv[frm])
        return p[kp_inv[to]][0]

    path = []
    for frm, to in pairwise('A' + seq):
        path += unsorted_path(frm, to)

    moves = path_to_moves(path)

    def apsort(path):
        atpt = kp_inv['A']
        res = []
        for sp in path.split('A'):
            cnt = Counter(sp)
            if 'v' in cnt and '<' in cnt and (atpt == kp_inv['^'] or (atpt == kp_inv['A'] and cnt['<'] > 1)):
                pat = 'v<'
            elif '^' in cnt and '>' in cnt and atpt == kp_inv['<']:
                pat = '>^'
            else:
                pat = '<v^>'
            res += [condense(cnt, pat)]
            atpt += sum(inv_char[x] for x in sp)
        return 'A'.join(res)

    return apsort(moves)


def part1(output=False):
    lines = parse()

    tot = 0
    for seq in lines:
        btn = kp_to_arrow(seq)
        btn = repeatedly_apply(arrow_to_arrow, btn, 2)
        num_part = int(''.join(c for c in seq if c in string.digits))
        tot += num_part * len(btn)

    return tot

def part2(output=False):
    lines = parse()

    tot = 0
    for seq in lines:
        if output:
            print('Starting seq', seq)
        btn = kp_to_arrow(seq)
        have_cnt = {sp + 'A': 1 for sp in btn.split('A')}
        have_cnt['A'] -= 1
        for it in range(25):
            have_upd = {}
            for hk, hv in have_cnt.items():
                if hk == 'A':
                    have_upd['A'] = have_upd.get('A', 0) + hv
                    continue
                res = arrow_to_arrow(hk)
                for sp in res.split('A'):
                    have_upd[sp + 'A'] = have_upd.get(sp + 'A', 0) + hv
                have_upd['A'] -= hv
            have_cnt = have_upd
            if output:
                print('Iteration:', it, 'has:', have_cnt)

        all_parts_len = sum(len(dk) * dv for dk, dv in have_cnt.items())
        num_part = int(''.join(c for c in seq if c in string.digits))
        tot += num_part * all_parts_len

    return tot

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
