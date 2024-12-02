from itertools import product

def parse():
    with open('data/aoc_2019/02.txt') as f:
        dat = [x.strip() for x in f.readlines()]
    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def run_program(base_program, noun, verb):
    program = list(base_program)
    pc = 0

    program[1] = noun
    program[2] = verb

    while True:
        opcode = program[pc]
        if opcode == 1:
            lhs  = program[program[pc + 1]]
            rhs  = program[program[pc + 2]]
            dest = program[pc + 3]
            program[dest] = lhs + rhs
            pc += 4
        elif opcode == 2:
            lhs  = program[program[pc + 1]]
            rhs  = program[program[pc + 2]]
            dest = program[pc + 3]
            program[dest] = lhs * rhs
            pc += 4
        elif opcode == 99:
            break
        else:
            print(f'Critical failure, unknown opcode {opcode}')
            exit()

    return program[0]

def part1(output=False):
    base_program = parse()
    return run_program(base_program, 12, 2)

def part2(output=False):
    base_program = parse()
    for noun, verb in product(range(100), repeat=2):
        result = run_program(base_program, noun, verb)
        if result == 19690720:
            return 100 * noun + verb

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
