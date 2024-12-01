with open('data/aoc_2016/12.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def regval(regs, itm):
    if itm in regs:
        return regs[itm]
    return int(itm)

def crunch(cval):
    regs = {i: 0 for i in 'abcd'}
    regs['c'] = cval
    pc = 0
    while True:
        if pc < 0 or pc >= len(dat):
            break
        d = dat[pc]
        if 'inc' in d:
            regs[d[-1]] += 1
        elif 'dec' in d:
            regs[d[-1]] -= 1
        elif 'cpy' in d:
            a, b = d.split(' ')[1:]
            regs[b] = regval(regs, a)
        elif 'jnz' in d:
            a, b = d.split(' ')[1:]
            if regval(regs, a) != 0:
                pc += int(b)
                continue
        else:
            print('Bad inst!')
        pc += 1
    return regs['a']

def part1(output = True):
    del output
    return crunch(0)

def part2(output = True):
    del output
    return crunch(1)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
