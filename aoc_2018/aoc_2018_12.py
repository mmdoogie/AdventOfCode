with open('data/aoc_2018/12.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output = True):
    state_str = dat[0].split(': ')[1]
    pattern_bits = [l.split(' => ') for l in dat[2:]]
    patterns = {l[0]: l[1] for l in pattern_bits}
    leftmost = 0

    if output:
        print('Initial State:', state_str, 'leftmost', leftmost)
    for gen in range(20):
        state_str = '...' + state_str + '...'
        new_state = ''
        leftmost -= 1
        for i in range(2, len(state_str) - 2):
            new_state += patterns[state_str[i-2:i+3]]
        state_str = new_state
        if output:
            print('New State:    ', state_str[-leftmost+gen:], 'leftmost', leftmost, 'gen', gen)

    return sum([i+leftmost if c == '#' else 0 for i, c in enumerate(state_str)])

def part2(output = True):
    state_str = dat[0].split(': ')[1]
    pattern_bits = [l.split(' => ') for l in dat[2:]]
    patterns = {l[0]: l[1] for l in pattern_bits}
    leftmost = 0

    scores = []
    gen = 0
    while True:
        gen += 1
        state_str = '...' + state_str + '...'
        new_state = ''
        leftmost -= 1
        for i in range(2, len(state_str) - 2):
            new_state += patterns[state_str[i-2:i+3]]
        score = sum([i+leftmost if c == '#' else 0 for i, c in enumerate(new_state)])
        scores += [score]
        if len(scores) > 20:
            last_delta = scores[-1] - scores[-2]
            delta = [scores[i] - scores[i-1] for i in range(-10, 0)]
            if all([d == last_delta for d in delta]):
                if output:
                    print('Stability found at gen', gen, '10 scores', scores[-10:])
                break
        state_str = new_state

    return scores[-1] + (50_000_000_000 - gen) * last_delta

