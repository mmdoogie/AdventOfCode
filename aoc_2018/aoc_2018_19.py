import math
from collections import namedtuple

with open('data/aoc_2018/19.txt', encoding='utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

Opcode = namedtuple('Opcode', ['a_val', 'b_val', 'fn', 'fmt'])

class ProgramLine:
    def __init__(self, opcode, ip_reg, *params):
        self.opcode = opcode
        self.ip_reg = ip_reg
        self.a = params[0]
        self.b = params[1]
        self.c = params[2]

    def execute(self, regfile):
        aa = self.a if self.opcode.a_val else regfile[self.a]
        bb = self.b if self.opcode.b_val else regfile[self.b]
        regfile[self.c] = self.opcode.fn(aa, bb)

    def __repr__(self):
        aa = self.a if self.opcode.a_val or self.a != self.ip_reg else 'ip'
        bb = self.b if self.opcode.b_val or self.b != self.ip_reg else 'ip'
        cc = self.c if self.c != self.ip_reg else 'ip'

        return self.opcode.fmt % (cc, aa, bb)

opcodes = {
    'addr': Opcode(False, False, lambda a, b: a + b, 'r%s = r%s + r%s'),
    'addi': Opcode(False, True,  lambda a, b: a + b, 'r%s = r%s + %s' ),
    'mulr': Opcode(False, False, lambda a, b: a * b, 'r%s = r%s * r%s'),
    'muli': Opcode(False, True,  lambda a, b: a * b, 'r%s = r%s * %s' ),
    'banr': Opcode(False, False, lambda a, b: a & b, 'r%s = r%s & r%s'),
    'bani': Opcode(False, True,  lambda a, b: a & b, 'r%s = r%s & %s' ),
    'borr': Opcode(False, False, lambda a, b: a | b, 'r%s = r%s | r%s'),
    'bori': Opcode(False, True,  lambda a, b: a | b, 'r%s = r%s | %s' ),
    'setr': Opcode(False, True,  lambda a, b: a,     'r%s = r%s  #unused: %s'),
    'seti': Opcode(True,  True,  lambda a, b: a,     'r%s = %s   #unused: %s'),
    'gtir': Opcode(True,  False, lambda a, b: 1 if a > b else 0,  'r%s = %s > r%s'  ),
    'gtri': Opcode(False, True,  lambda a, b: 1 if a > b else 0,  'r%s = r%s > %s'  ),
    'gtrr': Opcode(False, False, lambda a, b: 1 if a > b else 0,  'r%s = r%s > r%s' ),
    'eqir': Opcode(True,  False, lambda a, b: 1 if a == b else 0, 'r%s = %s == r%s' ),
    'eqri': Opcode(False, True,  lambda a, b: 1 if a == b else 0, 'r%s = r%s == %s' ),
    'eqrr': Opcode(False, False, lambda a, b: 1 if a == b else 0, 'r%s = r%s == r%s'),
}

def parse_prog(output = False):
    assert dat[0][0] == '#'
    ip_reg = int(dat[0].split(' ')[1])

    prog_lines = {}
    for i, d in enumerate(dat[1:]):
        mnemonic, *params = d.split(' ')
        opcode = opcodes[mnemonic]
        line = ProgramLine(opcode, ip_reg, *[int(x) for x in params])
        prog_lines[i] = line

    if output:
        print('Program listing:')
        for k, v in prog_lines.items():
            print(f'[{k:02d}] {v}')

    return prog_lines, ip_reg

def run_prog(prog_lines, ip_reg, reg1_val, output = False, short_circuit = False):
    reg = {0: reg1_val, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    while 0 <= reg[ip_reg] < len(prog_lines):
        prog_lines[reg[ip_reg]].execute(reg)
        reg[ip_reg] += 1
        if reg[ip_reg] == 1:
            if output:
                print('After init:', reg)
            if short_circuit:
                num = reg[4]
                max_factor = math.ceil(math.sqrt(num)) + 1
                return sum(x + num // x if num % x == 0 else 0 for x in range(1, max_factor))

    return reg[0]

def part1(output = True):
    prog_lines, ip_reg = parse_prog(output)
    fast_output = run_prog(prog_lines, ip_reg, 0, output = False, short_circuit = True)
    if output:
        print('Validating fast result vs raw run')
        raw_output = run_prog(prog_lines, ip_reg, 0, output = True, short_circuit = False)
        assert raw_output == fast_output
        print('OK')
    return fast_output

def part2(output = True):
    prog_lines, ip_reg = parse_prog(False)
    return run_prog(prog_lines, ip_reg, 1, output = False, short_circuit = True)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
