from itertools import combinations, product
import operator
import random

def parse():
    with open('data/aoc_2024/24.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    wires = {}
    ops = []
    for l in lines:
        if ':' in l:
            v = l.split(': ')
            wires[v[0]] = int(v[1])
        elif '->' in l:
            left, right = l.split(' -> ')
            ops += [(*left.split(' '), right)]
    return wires, ops

OPMAP = {'AND': operator.and_, 'OR': operator.or_, 'XOR': operator.xor}
def propagate(wires, ops):
    zs = [o[3] for o in ops if o[3].startswith('z')]

    while any(z not in wires for z in zs):
        prop = False
        for o in ops:
            if o[0] in wires and o[2] in wires and o[3] not in wires:
                wires[o[3]] = OPMAP[o[1]](wires[o[0]], wires[o[2]])
                prop = True
        if not prop:
            return None

    bin_str = ''.join(str(wires[b]) for b in sorted(zs, reverse=True))
    return bin_str

def part1(output=False):
    wires, ops = parse()
    val = propagate(wires, ops)
    return int(val, 2)

def phase_1(xs, ys, ops, output):
    if output:
        print('\nPhase 1: Single bit input mapping')

    bad_bits = []
    for x in xs:
        wires = {k: 1 if k == x else 0 for k in xs + ys}
        v = propagate(wires, ops)
        fail = wires[f'z{x[1:]}'] != 1
        if output:
            print(f'{x} -> {v} {"err" if fail else ""}')
        if fail:
            bad_bits += [x[1:]]
    return bad_bits

def phase_2(ops, bad_bits, output):
    if output:
        print('\nPhase 2: Trace intersection of forward and reverse propagation')

    cand_swap = {}
    for c in bad_bits:
        fwd_propset = set()
        inps = [f'x{c}']
        while True:
            to_add = set()
            for o in ops:
                if o[0] in inps or o[2] in inps:
                    if o not in fwd_propset:
                        to_add.add(o)
            if not to_add:
                break
            fwd_propset |= to_add
            inps += [o[3] for o in to_add]

        rev_propset = set()
        inps = [f'z{c}', f'z{int(c) + 1:02d}']
        while True:
            to_add = set()
            for o in ops:
                if o[3] in inps:
                    if o not in rev_propset:
                        to_add.add(o)
            if not to_add:
                break
            rev_propset |= to_add
            inps += [o[0] for o in to_add]
            inps += [o[2] for o in to_add]

        overlap = fwd_propset & rev_propset

        if output:
            print(f'x{c} propagates to {len(fwd_propset)} gates')
            print(f'z{c} & z{int(c) + 1:02d} propagate from {len(rev_propset)} gates')
            print(f'Overlap: {len(overlap)} gates')

        cand_swap[c] = overlap
    return cand_swap

def phase_3(xs, ys, gate_outs, cand_swap, output):
    if output:
        print('\nPhase 3: Look for single bit repairs in all pairs of phase 2 intersections')

    final_cand = {c: [] for c in cand_swap}
    for c, inter in cand_swap.items():
        for o1, o2 in combinations(inter, 2):
            wires = {k: 1 if k == f'x{c}' else 0 for k in xs + ys}
            ops = [v for k, v in gate_outs.items() if k not in {o1[3], o2[3]}]
            ops += [(*o1[:3], o2[3]), (*o2[:3], o1[3])]
            v = propagate(wires, ops)
            if v is None:
                continue
            if int(v, 2) == 1 << int(c):
                if output:
                    print('Candidate for bit', c, o1, o2)
                final_cand[c] += [(o1, o2)]
    return final_cand

def phase_4(xs, ys, gate_outs, final_cand, output):
    if output:
        print('\nPhase 4: Use random sums to eliminate inconsistent repairs')

    remain = set(product(*final_cand.values()))
    overprove = 100
    while len(remain) > 1 or overprove > 0:
        elim = set()
        for swaps in remain:
            wires = {k: 0 for k in xs + ys}
            x_val = 0
            y_val = 0
            for x, y in zip(xs, ys):
                wires[x] = random.randint(0, 1)
                wires[y] = random.randint(0, 1)
                x_val = (x_val << 1) + wires[x]
                y_val = (y_val << 1) + wires[y]
            target = x_val + y_val

            ops = [v for k, v in gate_outs.items() if k not in {ss[3] for s in swaps for ss in s}]
            for o1, o2 in swaps:
                ops += [(*o1[0:3], o2[3]), (*o2[0:3], o1[3])]
            v = propagate(wires, ops)
            if v is None or int(v, 2) != target:
                elim.add(swaps)
                if output:
                    if v is None:
                        v_str = f'{"Unsatisfiable":<16}'
                    else:
                        v_str = f'{int(v, 2):<16}'
                    print(f'Elim {x_val:<16} + {y_val:<16} == {target:<16} got {v_str:<16}; {len(remain)-len(elim)} remaining')
        remain -= elim
        if len(remain) == 1:
            overprove -= 1
    return remain.pop()

def part2(output=False):
    wires, ops = parse()

    xs = sorted([w for w in wires if w.startswith('x')], reverse=True)
    ys = sorted([w for w in wires if w.startswith('y')], reverse=True)
    gate_outs = {o[3]: o for o in ops}

    bad_bits = phase_1(xs, ys, ops, output)
    cand_swap = phase_2(ops, bad_bits, output)
    final_cand = phase_3(xs, ys, gate_outs, cand_swap, output)
    repair = phase_4(xs, ys, gate_outs, final_cand, output)

    return ','.join(sorted(ss[3] for s in repair for ss in s))

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
