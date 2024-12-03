from functools import cache
from itertools import product

with open('data/aoc_2023/12.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def satisfied(pattern, groups):
    return [len(x) for x in pattern.split('.') if '#' in x] == groups

def possible_arrangements(line):
    pattern, groups = line.split(' ')
    groups = [int(x) for x in groups.split(',')]

    q_pos = [i for i, c in enumerate(pattern) if c == '?']
    cnt = 0
    for p in product('.#', repeat = len(q_pos)):
        try_pattern = list(pattern)
        for q_idx, p_val in zip(q_pos, p):
            try_pattern[q_idx] = p_val
        try_pattern = ''.join(try_pattern)
        if satisfied(try_pattern, groups):
            cnt += 1

    return cnt

def part1(output = True):
    if output:
        print('Doing it the slow way...')
        return sum(possible_arrangements(l) for l in dat)
    return sum(solve(*expand_line(l, times = 1), None) for l in dat)

@cache
def solve(pattern, groups, remain_run):
    # Out of groups: fail if still unfulfilled pattern, otherwise success!
    if groups == ():
        if '#' in pattern:
            return 0
        return 1

    # Require a . or ? if run just ended
    if remain_run == 0:
        if pattern != '' and pattern[0] == '#':
            return 0
        return solve(pattern[1:], groups[1:], None)

    # Ran out of pattern with unfulfilled groups
    if pattern == '' and groups != ():
        return 0

    # Fail if we get a . while on a run, otherwise just pass on by
    if pattern[0] == '.':
        if remain_run:
            return 0
        return solve(pattern[1:], groups, None)

    # If we got a ? on a run, ok, continue
    # If not on a run, two options: start run or skip
    if pattern[0] == '?':
        if remain_run:
            return solve(pattern[1:], groups, remain_run - 1)
        return solve(pattern[1:], groups, groups[0] - 1) + solve(pattern[1:], groups, None)

    # If we got a # on a run, ok, continue
    # If not on a run, must start run
    if pattern[0] == '#':
        if remain_run:
            return solve(pattern[1:], groups, remain_run - 1)
        return solve(pattern[1:], groups, groups[0] - 1)

    assert pattern[0] in '.?#'
    return 0

def expand_line(line, times = 5):
    pattern, groups = line.split(' ')
    expand_pattern = '?'.join([pattern] * times)
    expand_groups = tuple([int(x) for x in groups.split(',')] * times)

    return expand_pattern, expand_groups

def part2(output = True):
    total_ways = 0

    for line in dat:
        pattern, groups = expand_line(line)
        ways =  solve(pattern, groups, None)
        total_ways += ways

        if output:
            grp_str = ','.join(str(g) for g in groups)
            print(f'{pattern:110s} {grp_str:65s} {ways}')

    return total_ways

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
