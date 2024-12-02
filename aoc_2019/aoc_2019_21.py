from aoc_2019.intcode import IntcodeComputer, PartialResult, IOMode

def parse():
    with open('data/aoc_2019/21.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def run_springscript(script):
    base_program = parse()
    ic = IntcodeComputer(base_program, io_mode = IOMode.ASCII)
    res = ic.run_partial()
    out = ic.all_outputs()
    ic.queue_inputs('\n'.join(script) + '\n')
    res = ic.run_partial()
    out1 = ic.out_deque.pop()
    if out1 > 256:
        return out1

def part1(output=False):
    return run_springscript(['OR A T', 'AND B T', 'AND C T', 'AND D T', 'NOT T J', 'AND D J', 'WALK'])

def part2(output=False):
    return run_springscript(['OR A T', 'AND B T', 'AND C T', 'AND D T', 'NOT T J', 'AND D J', 'AND H J', 'NOT A T', 'OR T J', 'RUN'])

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
