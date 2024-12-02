from itertools import combinations
from aoc_2019.intcode import IntcodeComputer, PartialResult, IOMode

def parse():
    with open('data/aoc_2019/17.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def compute_part1(output = False):
    base_program = parse()
    ic = IntcodeComputer(base_program, io_mode = IOMode.ASCII)
    rc = ic.run_partial()
    assert rc == PartialResult.TERMINATED
    out = ic.all_outputs()

    y = 0
    x = 0
    scaffold = {}

    for o in out:
        if o == '\n':
            x = 0
            y += 1
            if output:
                print()
            continue
        
        if o == '#':
            scaffold[(x, y)] = True

        if o == '^':
            start_pt = (x, y)
            start_dir = (0, -1)
        elif o == 'v':
            start_pt = (x, y)
            start_dir = (0, 1)
        elif o == '<':
            start_pt = (x, y)
            start_dir = (-1, 0)
        elif o == '>':
            start_pt = (x, y)
            start_dir = (1, 0)

        if output:
            print(o, end='')
        x += 1

    total = 0
    for sx, sy in scaffold.keys():
        adj = [(sx-1, sy), (sx+1, sy), (sx, sy-1), (sx, sy+1)]
        if sum([a in scaffold for a in adj]) >= 3:
            total += sx*sy

    return total, scaffold, start_pt, start_dir

def part1(output=False):
    total, _, _, _ = compute_part1(output)
    return total

def traverse(scaffold, start_pt, start_dir):
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    didx = dirs.index(start_dir)

    x, y = start_pt
    path = []

    while True:
        tcx, tcy = dirs[(didx - 1) % 4]
        if (x + tcx, y + tcy) in scaffold:
            turn = -1
            pc = 'L'
        else:
            tcx, tcy = dirs[(didx + 1) % 4]
            if (x + tcx, y + tcy) not in scaffold:
                break
            turn = 1
            pc = 'R'

        didx = (didx + turn) % 4

        cnt = 0
        while True:
            x += tcx
            y += tcy
            if (x, y) not in scaffold:
                x -= tcx
                y -= tcy
                break
            cnt += 1
        path += [pc + ',' + str(cnt)]

    return path

def find_solution(full_path):
    matches = []
    pathlen = len(full_path)
    for i, p in enumerate(full_path):
        maxlen = 0
        for j in range(i + 1, pathlen):
            subpath = ','.join(full_path[i:j])
            if len(subpath) > 20:
                break
            if subpath in ','.join(full_path[i+1:]):
                if len(subpath) > maxlen:
                    maxlen = len(subpath)
                    maxmatch = subpath
        if maxlen > 0 and maxmatch not in matches:
            matches += [maxmatch]

    matches.sort(key=lambda x: len(x), reverse=True)

    for subs in combinations(matches, 3):
        res = ','.join(full_path)
        for i, s in enumerate(subs):
            repl = chr(ord('A') + i)
            res = res.replace(s, repl)
        if 'L' in res or 'R' in res:
            continue
        return subs, res

def compute_part2(scaffold, start_pt, start_dir, output = False):
    full_path = traverse(scaffold, start_pt, start_dir)
    final_trav = ','.join(full_path)
    if output:
        print(final_trav)

    subs, res = find_solution(full_path)

    base_program = parse()
    p = list(base_program)
    p[0] = 2
    ic = IntcodeComputer(p, io_mode = IOMode.ASCII)
    rc = ic.run_partial()
    assert rc == PartialResult.WAIT_INPUT

    if output:
        print(ic.all_outputs(), end=' ')
        print(res)
    ic.queue_inputs(res + '\n')

    for s in subs:
        rc = ic.run_partial()
        assert rc == PartialResult.WAIT_INPUT
        if output:
            print(ic.all_outputs(), end=' ')
            print(s)
        ic.queue_inputs(s + '\n')

    rc = ic.run_partial()
    assert rc == PartialResult.WAIT_INPUT

    noline = 'n'
    if output:
        print(ic.all_outputs(), end=' ')
        print(noline)
    ic.queue_inputs(noline + '\n')
    rc = ic.run_partial()
    assert rc == PartialResult.TERMINATED

    rv = ic.out_deque.pop()
    if output:
        print(ic.all_outputs(), rv)
    return rv

def part2(output=False):
    _, scaffold, start_pt, start_dir = compute_part1(False)
    res = compute_part2(scaffold, start_pt, start_dir)
    return res

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
