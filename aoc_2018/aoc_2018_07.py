import re
from collections import deque

with open('data/aoc_2018/07.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output = True):
    pattern = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin')

    pairs = [tuple(pattern.match(d).groups()) for d in dat]
    all_steps = set([p[0] for p in pairs] + [p[1] for p in pairs])

    prereqs = {s: set() for s in all_steps}
    for before, after in pairs:
        prereqs[after].add(before)

    order = []
    while len(order) < len(all_steps):
        doable = sorted([k for k, v in prereqs.items() if len(v) == 0 and k not in order])
        doing = doable[0]
        order += [doing]
        for s in prereqs.values():
            if doing in s:
                s.remove(doing)

    return ''.join(order)

def part2(output = True):
    pattern = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin')

    pairs = [tuple(pattern.match(d).groups()) for d in dat]
    all_steps = set([p[0] for p in pairs] + [p[1] for p in pairs])

    prereqs = {s: set() for s in all_steps}
    for before, after in pairs:
        prereqs[after].add(before)

    order = []
    elves = 5
    t_plus = 60
    elf_times = [0] * elves
    elf_tasks = [None] * elves
    t = 0
    while len(order) < len(all_steps):
        available = [et <= t for et in elf_times]
        if sum(available) == 0:
            t += 1
            continue
        if output:
            before_order = ''.join(order)
            out_str = f't:{t} available:{sum(available)}, elves: {elf_times} {elf_tasks} '
        for i in range(elves):
            if not available[i] or elf_tasks[i] is None:
                continue
            done = elf_tasks[i]
            elf_tasks[i] = None
            order += [done]
            for s in prereqs.values():
                if done in s:
                    s.remove(done)
        doable = deque(sorted([k for k, v in prereqs.items() if len(v) == 0 and k not in order and k not in elf_tasks]))
        if output:
            if len(doable) > 0 or before_order != ''.join(order):
                print(out_str, end = '')
            else:
                out_str = ''
        for i in range(elves):
            if not available[i]:
                continue
            if len(doable) == 0:
                break
            task = doable.popleft()
            elf_tasks[i] = task
            elf_times[i] = t + t_plus + ord(task) - ord('A') + 1
        if output and out_str != '':
            print(''.join(order), elf_times, elf_tasks)
        t += 1

    return t - 1
