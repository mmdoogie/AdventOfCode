with open('data/aoc_2017/04.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    del output

    words = [d.split(' ') for d in dat]
    valid = len([True for w in words if len(set(w)) == len(w)])
    return valid

def part2(output = True):
    del output

    words = [[''.join(sorted(w)) for w in d.split(' ')] for d in dat]
    valid = len([True for w in words if len(set(w)) == len(w)])
    return valid

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
