from mrm.cpoint import ZERO, UP, DOWN, LEFT, RIGHT

with open('data/aoc_2015/03.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
MOVES = {'^': UP, 'v': DOWN, '<': LEFT, '>': RIGHT}

def part1(output = True):
    loc = ZERO
    visited = set([loc])
    for m in dat[0]:
        loc += MOVES[m]
        visited.add(loc)
    return len(visited)

def part2(output = True):
    loc = ZERO
    visited = set([loc])
    for m in dat[0][0::2]:
        loc += MOVES[m]
        visited.add(loc)
    loc = ZERO
    for m in dat[0][1::2]:
        loc += MOVES[m]
        visited.add(loc)
    return len(visited)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
