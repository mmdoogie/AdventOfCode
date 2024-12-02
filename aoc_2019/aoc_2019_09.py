from aoc_2019.intcode import IntcodeComputer, PartialResult

def parse():
    with open('data/aoc_2019/09.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def part1(output=False):
    base_program = parse()
    ic = IntcodeComputer(base_program)
    ic.input(1)
    res = ic.run_partial()
    assert res == PartialResult.TERMINATED
    return ic.output()


def part2(output=False):
    base_program = parse()
    ic = IntcodeComputer(base_program)
    ic.input(2)
    res = ic.run_partial()
    assert res == PartialResult.TERMINATED
    return ic.output()

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
