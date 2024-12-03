from functools import reduce
import operator
import re

with open('data/aoc_2023/19.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse(output = False):
    workflows = {}
    parts = []

    wf_re = re.compile('([xmas])([><])([0-9]+):([a-zAR]+)|([a-zAR]+)')

    for d in dat:
        if d == '':
            continue
        if d[0] == '{':
            params = tuple(int(v[2:]) for v in d.split('{')[1].split('}')[0].split(','))
            parts += [params]
            if output:
                print(d, '==>', params)
        else:
            name = d.split('{')[0]
            flow_txt = d.split('{')[1].split('}')[0].split(',')
            flows = []
            for ft in flow_txt:
                flows += [wf_re.match(ft).groups()]
            workflows[name] = flows
            if output:
                print(d, '==>', flows)

    return parts, workflows

OP_MAP = {'<': operator.lt, '>': operator.gt}
PARAM_ORDER = 'xmas'

def part1(output = True):
    parts, flows = parse(output)

    accept_val = 0
    for p in parts:
        if output:
            print(p, end='')
        flow = 'in'
        while True:
            if output:
                print('', flow, end='')
            for f_param, f_op, f_val, f_dest, f_default in flows[flow]:
                if f_default is not None:
                    flow = f_default
                    break
                if OP_MAP[f_op](p[PARAM_ORDER.index(f_param)], int(f_val)):
                    flow = f_dest
                    break
            if flow in 'AR':
                accept = flow == 'A'
                break
        if output:
            print(' ACCEPT' if accept else ' REJECT')
        if accept:
            accept_val += sum(v for v in p)

    return accept_val

def split_ranges(flows, flow, ranges):
    res = {}
    for f_param, f_op, f_val, f_dest, f_default in flows[flow]:
        if f_default is not None:
            if f_default in 'AR':
                res[ranges] = f_default
            else:
                res.update(split_ranges(flows, f_default, ranges))
            break
        param_i = PARAM_ORDER.index(f_param)
        match f_op:
            case '<':
                remap  = tuple(a if i != param_i else (a[0],       int(f_val) - 1) for i, a in enumerate(ranges))
                ranges = tuple(a if i != param_i else (int(f_val), a[1])           for i, a in enumerate(ranges))
            case '>':
                remap  = tuple(a if i != param_i else (int(f_val) + 1, a[1])       for i, a in enumerate(ranges))
                ranges = tuple(a if i != param_i else (a[0],           int(f_val)) for i, a in enumerate(ranges))
        if f_dest in 'AR':
            res[remap] = f_dest
        else:
            res.update(split_ranges(flows, f_dest, remap))
    return res

def part2(output = True):
    _, flows = parse()

    init_ranges = ((1, 4000),) * 4
    sub_ranges = split_ranges(flows, 'in', init_ranges)

    accept_cnt = 0
    for sub_range, result in sub_ranges.items():
        if result == 'A':
            span = reduce(operator.mul, [param_range[1] - param_range[0] + 1 for param_range in sub_range])
            accept_cnt += span
            if output:
                print('sub range:', sub_range, 'has span:', span, 'total accepted:', accept_cnt)

    if output:
        print('Total sub ranges:', len(sub_ranges))

    return accept_cnt

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
