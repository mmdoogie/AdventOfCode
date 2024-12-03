from collections import defaultdict, deque
import math

with open('data/aoc_2023/20.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    nodes = {}
    nn = set()
    for d in dat:
        src, dst = d.split(' -> ')
        if src == 'broadcaster':
            src_name = src
            src_type = None
        else:
            src_type, src_name = src[0], src[1:]
        dst = dst.split(', ')
        nodes[src_name] = (src_type, dst)
        nn.add(src_name)
        nn.update(dst)

    inputs = defaultdict(list)
    for n in list(nodes.keys()) + ['rx']:
        for k, v in nodes.items():
            if n in v[1]:
                inputs[n] += [k]

    return nodes, inputs

def push_button(nodes, inputs, memory):
    signals = deque()

    signals.append(('broadcaster', 'low', 'button'))

    high_cnt, low_cnt = 0, 1
    while len(signals) != 0:
        sig = signals.popleft()
        if sig[0] == 'rx':
            continue

        n = nodes[sig[0]]
        match n[0]:
            case None:
                for o in n[1]:
                    signals.append((o, 'low', sig[0]))
                    low_cnt += 1
            case '&':
                m = memory.get(sig[0], {k: 'low' for k in inputs[sig[0]]})
                m[sig[2]] = sig[1]
                memory[sig[0]] = m
                val = all(mv == 'high' for mv in m.values())
                for o in n[1]:
                    signals.append((o, 'low' if val else 'high', sig[0]))
                    if val:
                        low_cnt += 1
                    else:
                        high_cnt += 1
            case '%':
                m = memory.get(sig[0], False)
                if sig[1] == 'low':
                    memory[sig[0]] = not m
                    for o in n[1]:
                        signals.append((o, 'low' if m else 'high', sig[0]))
                        if m:
                            low_cnt += 1
                        else:
                            high_cnt += 1
    return high_cnt, low_cnt

def part1(output = True):
    nodes, inputs = parse()
    memory = {}

    high_cnt, low_cnt = 0, 0
    for i in range(1000):
        hc, lc = push_button(nodes, inputs, memory)
        high_cnt += hc
        low_cnt += lc
        if output:
            print(f'Button press {i + 1:4d} --> High: {hc:4d} + Low: {lc:4d}')

    if output:
        print('Total High:', high_cnt, 'Low:', low_cnt)

    return high_cnt * low_cnt

def part2(output = True):
    nodes, inputs = parse()

    feed_node = inputs['rx'][0]
    counter_nodes = [inputs[a][0] for a in inputs[feed_node]]

    memory = {}
    clock_node = {}
    first_max = {}
    second_max = {}
    confirmed = {cn: False for cn in counter_nodes}

    it = 0
    while True:
        it += 1
        push_button(nodes, inputs, memory)

        for cn in counter_nodes:
            if it == 1:
                clock_node[cn] = [k for k, v in memory[cn].items() if v == 'high'][0]
            if all(v == 'high' for k, v in memory[cn].items() if k != clock_node[cn]):
                if cn not in first_max:
                    first_max[cn] = it
                    if output:
                        print('First max', cn, it)
                    continue
                if cn not in second_max:
                    second_max[cn] = it
                    if output:
                        print('Second max', cn, it)
                    continue
                assert it - second_max[cn] == second_max[cn] - first_max[cn]
                confirmed[cn] = True
                if output:
                    print('Confirmed', cn)
        if all(confirmed.values()):
            break

    loop_lens = {cn: second_max[cn] - first_max[cn] for cn in counter_nodes}
    if output:
        print('Loop lengths:', loop_lens)

    return math.lcm(*loop_lens.values())

if __name__ == '__main__':
    print('Part 2:', part2(True))
