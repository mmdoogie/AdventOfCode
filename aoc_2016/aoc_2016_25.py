with open('data/aoc_2016/25.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def regval(regs, itm):
    if itm in regs:
        return regs[itm]
    return int(itm)

def crunch(aval, output):
    regs = {i: 0 for i in 'abcd'}
    instrs = list(dat)

    regs['a'] = aval
    pc = 0
    last_out = 1
    good_outs = 0
    while True:
        if pc < 0 or pc >= len(dat):
            break
        d = instrs[pc]
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
                pc += regval(regs, b)
                continue
        elif 'tgl' in d:
            a = regval(regs, d.split(' ')[1])
            if pc + a >= len(dat):
                pc += 1
                continue
            modline = instrs[pc + a]
            if 'inc' in modline:
                modline = 'dec' + modline[3:]
            elif 'dec' in modline or 'tgl' in modline:
                modline = 'inc' + modline[3:]
            elif 'jnz' in modline:
                modline = 'cpy' + modline[3:]
            elif 'cpy' in modline:
                modline = 'jnz' + modline[3:]
            else:
                print('Bad toggle!', d, modline)
            instrs[pc + a] = modline
        elif 'out' in d:
            if output:
                print(regval(regs, d[-1]), end=', ')
            if regval(regs, d[-1]) != 1-last_out:
                return False
            good_outs += 1
            last_out = 1-last_out
            if good_outs == 100:
                return True
        else:
            print('Bad inst!', d)
        pc += 1
    return regs['a']

def part1(output = True):
    i = 0
    while True:
        if output:
            print(i, end=': ')
        c = crunch(i, output)
        if output:
            print()
        if c:
            return i
        i += 1

def part2(output = True):
    del output
    return 'Transmit!'

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
