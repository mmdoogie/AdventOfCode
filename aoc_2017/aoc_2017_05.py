with open('data/aoc_2017/05.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    jmps = [int(x) for x in dat]

def modrule_part1(jlist, curr_idx, _next_jmp):
    jlist[curr_idx] += 1

def modrule_part2(jlist, curr_idx, next_jmp):
    if next_jmp >= 3:
        jlist[curr_idx] -= 1
    else:
        jlist[curr_idx] += 1

def traverse(modrule):
    jlist = list(jmps)
    jlist_size = len(jmps)
    curr_idx = 0
    steps = 0

    while True:
        next_jmp = jlist[curr_idx]
        modrule(jlist, curr_idx, next_jmp)
        curr_idx += next_jmp
        steps += 1
        if curr_idx >= jlist_size:
            break

    return steps

def part1(output = True):
    del output
    return traverse(modrule_part1)

def part2(output = True):
    del output
    return traverse(modrule_part2)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
