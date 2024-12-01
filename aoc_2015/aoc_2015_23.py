with open('data/aoc_2015/23.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def process(init_a):
    regs = {'a': init_a, 'b': 0}
    pc = 0
    while True:
        if pc < 0 or pc >= len(dat):
            break
        d = dat[pc]
        match d.split(' '):
            case ['hlf', r]:
                regs[r] /= 2
            case ['tpl', r]:
                regs[r] *= 3
            case ['inc', r]:
                regs[r] += 1
            case ['jmp', v]:
                pc += int(v.strip('+'))
                continue
            case ['jie', r, v]:
                if regs[r.strip(',')] % 2 == 0:
                    pc += int(v.strip('+'))
                    continue
            case ['jio', r, v]:
                if regs[r.strip(',')] == 1:
                    pc += int(v.strip('+'))
                    continue
        pc += 1
    return regs['b']

def part1(output = True):
    return process(0)

def part2(output = True):
    return process(1)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
