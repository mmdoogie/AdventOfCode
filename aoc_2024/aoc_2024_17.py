from z3 import BitVec, Solver, ULT, sat

from mrm.parse import all_nums

def parse():
    with open('data/aoc_2024/17.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def combo_operand(operand, registers):
    if operand == 7:
        raise ValueError('7 is invalid combo operand')
    if 0 <= operand <= 3:
        return operand
    return registers[{4: 'A', 5: 'B', 6: 'C'}[operand]]

def part1(output=False):
    lines = parse()

    registers = {'A': 0, 'B': 0, 'C': 0}
    for l in lines:
        if 'Register' in l:
            registers[l[9]] = next(all_nums(l))
        if 'Program' in l:
            program = list(all_nums(l))

    if output:
        print('Registers:', registers)
        print('Program:', program)

    pc = 0
    res = []

    while True:
        if pc >= len(program):
            break

        instr = program[pc]
        operand = program[pc + 1]

        if instr in [0, 6, 7]:
            registers[{0: 'A', 6: 'B', 7: 'C'}[instr]] = registers['A'] // (2 ** combo_operand(operand, registers))
        if instr == 1:
            registers['B'] = registers['B'] ^ operand
        if instr == 2:
            registers['B'] = combo_operand(operand, registers) % 8
        if instr == 3 and registers['A'] != 0:
            pc = operand - 2
        if instr == 4:
            registers['B'] = registers['B'] ^ registers['C']
        if instr == 5:
            res += [str(combo_operand(operand, registers) % 8)]

        pc += 2

    return ','.join(res)

def part2(output=False):
    lines = parse()

    for l in lines:
        if 'Program' in l:
            program = list(all_nums(l))

    solver = Solver()
    a_vars = []
    for i, p in enumerate(program):
        a_curr = BitVec(f'A{i}', 64)
        solver.add(((a_curr % 8) ^ program[3] ^ program[9] ^ (a_curr / (1 << ((a_curr % 8) ^ program[3])))) % 8 == p)
        if a_vars:
            solver.add(a_curr == a_vars[-1] / (2 ** program[7]))
        a_vars += [a_curr]
    solver.add(ULT(a_curr, 2 ** program[7]))

    if output:
        print('Solving', solver.assertions())
        print()

    while solver.check() == sat:
        model = solver.model()
        if output:
            print('Found', model)
            print('Adding A0 <', model[a_vars[0]])
            print()
        solver.add(ULT(a_vars[0], model[a_vars[0]]))

    if output:
        print('No further solutions')

    return model[a_vars[0]]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
