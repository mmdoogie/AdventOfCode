from itertools import permutations

with open('data/aoc_2016/03.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    tris = [[int(x) for x in d.split()] for d in dat]

def count_valid(sizes):
    return sum(all(a + b > c for a, b, c in permutations(s, 3)) for s in sizes)

def part1(output = True):
    del output
    return count_valid(tris)

def part2(output = True):
    del output
    regrp = [[tris[l][c], tris[l + 1][c], tris[l + 2][c]] for l in range(0, len(dat), 3) for c in range(3)]
    return count_valid(regrp)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
