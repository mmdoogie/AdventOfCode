with open('data/aoc_2021/24.txt', 'r') as f:
    dat = [x.strip().split(' ') for x in f.readlines()]

perchar = [dat[x:x+18] for x in range(0, len(dat), 18)]

def maxmodel(mnum):
    deps = []
    oidx = []
    for i, p in enumerate(perchar):
        if p[4][2] == '1':
            oidx += [i]
            deps += [mnum[i] + int(p[15][2])]
        else:
            c = deps.pop() + int(p[5][2])
            ci = oidx.pop()

            newc = max(1, min(c, 9))
            mnum[i] = newc
            mnum[ci] += (newc - c)

    return ''.join([str(x) for x in mnum])

def part1(output=False):
    return maxmodel([9] * 14)

def part2(output=False):
    return maxmodel([1] * 14)
