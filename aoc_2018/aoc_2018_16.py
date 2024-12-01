with open('data/aoc_2018/16.txt') as f:
    dat = [x.strip('\n') for x in f.readlines()]

class Opcode:
    def __init__(self, name, a_val, b_val, fn):
        self.name = name
        self.a_val = a_val
        self.b_val = b_val
        self.fn = fn

    def execute(self, a, b, c, regfile):
        if self.a_val:
            aa = a
        else:
            aa = regfile[a]

        if self.b_val:
            bb = b
        else:
            bb = regfile[b]

        return regfile[:c] + [self.fn(aa, bb)] + regfile[c + 1:]

opcodes = {
    'addr': Opcode('addr', False, False, lambda a, b: a + b),
    'addi': Opcode('addi', False, True,  lambda a, b: a + b),
    'mulr': Opcode('mulr', False, False, lambda a, b: a * b),
    'muli': Opcode('muli', False, True,  lambda a, b: a * b),
    'banr': Opcode('banr', False, False, lambda a, b: a & b),
    'bani': Opcode('bani', False, True,  lambda a, b: a & b),
    'borr': Opcode('borr', False, False, lambda a, b: a | b),
    'bori': Opcode('bori', False, True,  lambda a, b: a | b),
    'setr': Opcode('setr', False, False, lambda a, b: a),
    'seti': Opcode('seti', True,  False, lambda a, b: a),
    'gtir': Opcode('gtir', True,  False, lambda a, b: 1 if a > b else 0),
    'gtri': Opcode('gtri', False, True,  lambda a, b: 1 if a > b else 0),
    'gtrr': Opcode('gtrr', False, False, lambda a, b: 1 if a > b else 0),
    'eqir': Opcode('eqir', True,  False, lambda a, b: 1 if a == b else 0),
    'eqri': Opcode('eqri', False, True,  lambda a, b: 1 if a == b else 0),
    'eqrr': Opcode('eqrr', False, False, lambda a, b: 1 if a == b else 0),
}

def parse():
    examples = []
    prog = []
    section_2 = False
    for d in dat:
        if d.startswith('Before'):
            section_2 = False
            exa = {'before': [int(x) for x in d.split('[')[1].strip(']').split(',')]}
        elif d.startswith('After'):
            exa['after'] = [int(x) for x in d.split('[')[1].strip(']').split(',')]
            examples += [exa]
        elif not section_2 and d != '':
            exa['op'] = [int(x) for x in d.split(' ')]
        elif not section_2 and d == '':
            section_2 = True
        elif section_2 and d != '':
            prog += [[int(x) for x in d.split(' ')]]

    return examples, prog

def part1(output = True):
    exa, prog = parse()

    three_or_more = 0
    for e in exa:
        match = 0
        reg = e['before']
        for o in opcodes.values():
            out = o.execute(*e['op'][1:], reg)
            if out == e['after']:
                match += 1
        if match >= 3:
            three_or_more += 1
        if output:
            print(e['before'], e['op'], e['after'], 'matches', match, f'[{three_or_more}]')

    return three_or_more

def part2(output = True):
    exa, prog = parse()

    potentials = {}
    for e in exa:
        reg = e['before']
        matches = []
        opnum = e['op'][0]
        for o in opcodes.values():
            out = o.execute(*e['op'][1:], reg)
            if out == e['after']:
                matches += [o.name]
        if opnum in potentials:
            overlap = potentials[opnum].intersection(set(matches))
            potentials[opnum] = overlap
            if output:
                print(e['before'], e['op'], e['after'], 'matches', matches, 'overlaps', overlap)
        else:
            potentials[opnum] = set(matches)
            if output:
                print(e['before'], e['op'], e['after'], 'matches', matches)

    if output:
        print('Solved so far:', sum([len(v) == 1 for k, v in potentials.items()]))

    while True:
        for k, v in potentials.items():
            if len(v) == 1:
                sol = list(v)[0]
                elim = []
                for k2 in potentials.keys():
                    if k2 != k and sol in potentials[k2]:
                        potentials[k2].remove(sol)
                        if sol not in elim:
                            elim += [sol]
                if output and elim:
                    print('Back eliminated', elim)
        solved = sum([len(v) == 1 for k, v in potentials.items()])
        if output:
            print('Solved so far:', solved)
        if solved == len(potentials):
            break

    if output:
        print('Final opcode map:', potentials)
        print('Running test program')

    opmap = {k: opcodes[list(v)[0]] for k, v in potentials.items()}
    reg = [0, 0, 0, 0]
    if output:
        print(reg)
    for p in prog:
        reg = opmap[p[0]].execute(*p[1:], reg)
        if output:
            print(reg)

    return reg[0]
