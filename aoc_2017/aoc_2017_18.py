import asyncio
from collections import defaultdict

with open('data/aoc_2017/18.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def getval(regs, itm):
    if itm in 'abcdefghijklmnopqrstuvwxyz':
        return regs[itm]
    return int(itm)

def part1(output = True):
    pc = 0
    regs = defaultdict(int)

    last_snd = 0
    while True:
        instr = dat[pc].split(' ')
        if instr[0] == 'snd':
            last_snd = getval(regs, instr[1])
            if output:
                print('snd', last_snd)
        elif instr[0] == 'set':
            regs[instr[1]] = getval(regs, instr[2])
        elif instr[0] == 'add':
            regs[instr[1]] += getval(regs, instr[2])
        elif instr[0] == 'mul':
            regs[instr[1]] *= getval(regs, instr[2])
        elif instr[0] == 'mod':
            regs[instr[1]] = regs[instr[1]] % getval(regs, instr[2])
        elif instr[0] == 'rcv':
            if getval(regs, instr[1]) != 0:
                return last_snd
        elif instr[0] == 'jgz':
            if getval(regs, instr[1]) > 0:
                pc += getval(regs, instr[2])
                continue
        else:
            print('Undefined operation encountered!')
        pc += 1

    return 0

async def prog_body(pid, inq, outq, output):
    pc = 0
    regs = defaultdict(int)
    regs['p'] = pid

    snd_cnt = 0
    while True:
        if pc < 0 or pc > len(dat):
            break
        instr = dat[pc].split(' ')
        if instr[0] == 'snd':
            await outq.put(getval(regs, instr[1]))
            snd_cnt += 1
            if output:
                print(pid, '>', snd_cnt)
        elif instr[0] == 'set':
            regs[instr[1]] = getval(regs, instr[2])
        elif instr[0] == 'add':
            regs[instr[1]] += getval(regs, instr[2])
        elif instr[0] == 'mul':
            regs[instr[1]] *= getval(regs, instr[2])
        elif instr[0] == 'mod':
            regs[instr[1]] = regs[instr[1]] % getval(regs, instr[2])
        elif instr[0] == 'rcv':
            try:
                val = await asyncio.wait_for(inq.get(), timeout=0.1)
            except TimeoutError:
                outq.put_nowait(None)
                break
            if output:
                print(pid, '<', val)
            if val is None:
                break
            regs[instr[1]] = val
        elif instr[0] == 'jgz':
            if getval(regs, instr[1]) > 0:
                pc += getval(regs, instr[2])
                continue
        else:
            print('Undefined operation encountered!')
        pc += 1

    return snd_cnt

async def do_part2(output):
    q01 = asyncio.Queue()
    q10 = asyncio.Queue()

    t0 = asyncio.create_task(prog_body(0, q10, q01, output))
    t1 = asyncio.create_task(prog_body(1, q01, q10, output))

    await t0
    sent_1 = await t1

    return sent_1

def part2(output = True):
    res = asyncio.run(do_part2(output))
    return res

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
