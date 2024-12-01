from collections import defaultdict

with open('data/aoc_2017/23.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def getval(regs, itm):
    if itm in 'abcdefgh':
        return regs[itm]
    return int(itm)

def part1(output = True):
    del output

    pc = 0
    regs = defaultdict(int)

    mul_cnt = 0
    while True:
        if pc < 0 or pc >= len(dat):
            return mul_cnt
        instr = dat[pc].split(' ')
        if instr[0] == 'set':
            regs[instr[1]] = getval(regs, instr[2])
        elif instr[0] == 'sub':
            regs[instr[1]] -= getval(regs, instr[2])
        elif instr[0] == 'mul':
            regs[instr[1]] *= getval(regs, instr[2])
            mul_cnt += 1
        elif instr[0] == 'jnz':
            if getval(regs, instr[1]) != 0:
                pc += getval(regs, instr[2])
                continue
        else:
            print('Undefined operation encountered!')
        pc += 1

    return 0

def part2(output = True):
    pc = 0
    regs = defaultdict(int)
    regs['a'] = 1

    while True:
        instr = dat[pc].split(' ')
        if instr[0] == 'set':
            regs[instr[1]] = getval(regs, instr[2])
        elif instr[0] == 'sub':
            regs[instr[1]] -= getval(regs, instr[2])
        elif instr[0] == 'mul':
            regs[instr[1]] *= getval(regs, instr[2])
        elif instr[0] == 'jnz':
            if getval(regs, instr[1]) != 0:
                pc += getval(regs, instr[2])
                continue
        else:
            print('Undefined operation encountered!')
        if pc == 30:
            incr = regs['b']
            break
        if regs['f'] == 1:
            rb = regs['b']
            rc = regs['c']
            regs['b'] = 0
            pc = 29
        pc += 1

    if output:
        print(f'b: {rb}, c: {rc}, incr: {incr}')

    h = 0
    for v in range(rb, rc+1, incr):
        for d in range(2, round(pow(v, 0.5)) + 1):
            if v % d == 0:
                h += 1
                break

    return h

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
