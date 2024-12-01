import operator

with open('data/aoc_2015/07.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

class Gate:
    def __init__(self, wires, op, left, right, out):
        self.wires = wires
        self.left = left
        self.op = op
        self.right = right
        self.out = out
        self.done = False

    def is_ready(self):
        if self.get_wire(self.left) is None:
            return False
        if self.get_wire(self.right) is None:
            return False
        return True

    def get_wire(self, wire):
        if wire in self.wires:
            return self.wires[wire]
        try:
            lit = int(wire)
            return lit
        except ValueError:
            return None

    def process(self):
        self.wires[self.out] = self.op(self.get_wire(self.left), self.get_wire(self.right))
        self.done = True
        return self.out

    def is_done(self):
        return self.done

    def __repr__(self):
        return (f'{self.left:<5}  {self.op.__name__:6}  {self.right:<5} -> {self.out:5}'
                f'(d{"+" if self.done else "-"} r{"+" if self.is_ready() else "-"})')

def process(output, override = None):
    wires = {}
    waiting = set()
    op_map = {
        'PASS': operator.and_,
        'NOT': operator.xor,
        'AND': operator.and_,
        'OR' : operator.or_,
        'LSHIFT': operator.lshift,
        'RSHIFT': operator.rshift 
    }

    for d in dat:
        lhs, rhs = d.split(' -> ')
        try:
            wires[rhs] = int(lhs)
        except ValueError:
            lhs = lhs.split(' ')
            oper = 'PASS'
            rarg = 0xFFFF
            match lhs:
                case [larg]:
                    waiting.add(Gate(wires, op_map[oper], larg, rarg, rhs))
                case [oper, larg]:
                    waiting.add(Gate(wires, op_map[oper], larg, rarg, rhs))
                case [larg, oper, rarg]:
                    waiting.add(Gate(wires, op_map[oper], larg, rarg, rhs))

    if override is not None:
        wires['b'] = override

    while True:
        runnable = {g for g in waiting if g.is_ready()}
        for r in runnable:
            wire = r.process()
            if output:
                print(r)
            if wire == 'a':
                return wires['a']
        waiting -= runnable
        if output:
            print(f'Completed: {len(runnable)}, Waiting: {len(waiting)}')
            print()

    return wires['a']

def part1(output = True):
    return process(output)

def part2(output = True):
    p1 = process(False)
    return process(output, override = p1)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
