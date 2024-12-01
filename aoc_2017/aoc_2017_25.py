from collections import defaultdict

with open('data/aoc_2017/25.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    start_state = None
    step_count = None
    states = {}
    state_info = {}
    curr_state = None
    curr_val = None
    write_val = None
    slot_dir = None
    next_state = None
    for d in dat:
        if not start_state:
            start_state = d[-2]
            continue
        if not step_count:
            step_count = int(d.split(' ')[5])
            continue
        if d == '':
            continue
        if not curr_state:
            curr_state = d[-2]
            continue
        if curr_val is None:
            curr_val = int(d[-2])
            continue
        if write_val is None:
            write_val = int(d[-2])
            continue
        if not slot_dir:
            if 'right' in d:
                slot_dir = 1
            else:
                slot_dir = -1
            continue
        if not next_state:
            next_state = d[-2]
            state_info[curr_val] = {'write': write_val, 'move': slot_dir, 'next': next_state}
            if curr_val == 1:
                states[curr_state] = state_info
                state_info = {}
                curr_state = None
            curr_val = None
            write_val = None
            slot_dir = None
            next_state = None
            continue

def part1(output = True):
    del output

    state = start_state
    loc = 0
    tape = defaultdict(int)
    for _ in range(step_count):
        inf = states[state][tape[loc]]
        tape[loc] = inf['write']
        loc += inf['move']
        state = inf['next']

    return sum(tape.values())

def part2(output = True):
    del output

    return 'Reboot!'

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
