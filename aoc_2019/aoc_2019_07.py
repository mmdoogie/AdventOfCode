from itertools import permutations
from collections import namedtuple, deque
from enum import Enum
import asyncio

class ParamSrc(Enum):
    NONE = 0
    PROGRAM = 1
    INPUT = 2

class ResultDest(Enum):
    NONE = 0
    PROGRAM = 1
    OUTPUT = 2
    PC = 3

EvalResult = namedtuple('EvalResult', ['mem_change', 'output', 'new_pc'])

class Instr:
    def __init__(self, opcode, param_cnt, param_src, result_dest, eval_fun):
        self.opcode = opcode
        self.param_cnt = param_cnt
        self.param_src = param_src
        self.result_dest = result_dest
        self.eval_fun = eval_fun

    def eval(self, program, start_pc, inputs = []):
        pc = start_pc
        op = program[pc]
        assert op % 100 == self.opcode, 'Wrong opcode requested for eval'

        if op == 99:
            return EvalResult({}, [], None)

        pc += 1
        op = op // 10

        if self.param_src == ParamSrc.PROGRAM:
            params = []
            for i in range(self.param_cnt):
                op = op // 10
                param_mode = op % 10
                if param_mode == 0:
                    params += [program[program[pc + i]]]
                elif param_mode == 1:
                    params += [program[pc + i]]
                else:
                    assert False, 'Invalid param_mode for src'
            pc += self.param_cnt
        elif self.param_src == ParamSrc.INPUT:
            params = inputs
        elif self.param_src == ParamSrc.NONE:
            params = []
        else:
            assert False, 'Invalid ParamSrc'

        val = self.eval_fun(*params)

        if self.result_dest == ResultDest.PROGRAM:
            op = op // 10
            param_mode = op % 10
            if param_mode == 0:
                return EvalResult({program[pc]: val}, [], pc + 1)
            elif param_mode == 1:
                assert False, 'WTF'
                return EvalResult({program[pc]: val}, [], pc + 1)
            else:
                assert False, 'Invalid param_mode for dest'
        elif self.result_dest == ResultDest.OUTPUT:
            return EvalResult({}, [val], pc)
        elif self.result_dest == ResultDest.PC:
            if val:
                return EvalResult({}, [], params[-1])
            else:
                return EvalResult({}, [], pc)
        else:
            assert False, 'Invalid ResultDest'

IC_INSTRS = { 1:  Instr(1,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: a + b),
              2:  Instr(2,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: a * b),
              3:  Instr(3,  1, ParamSrc.INPUT,   ResultDest.PROGRAM, lambda a: a),
              4:  Instr(4,  1, ParamSrc.PROGRAM, ResultDest.OUTPUT,  lambda a: a),
              5:  Instr(5,  2, ParamSrc.PROGRAM, ResultDest.PC,      lambda a, b: a != 0),
              6:  Instr(6,  2, ParamSrc.PROGRAM, ResultDest.PC,      lambda a, b: a == 0),
              7:  Instr(7,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: 1 if a < b else 0),
              8:  Instr(8,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: 1 if a == b else 0),
              99: Instr(99, 0, ParamSrc.NONE,    ResultDest.NONE,    None) 
            }

def parse():
    with open('data/aoc_2019/07.txt') as f:
        dat = [x.strip() for x in f.readlines()]
    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def run_program(base_program, inp):
    program = list(base_program)
    pc = 0
    outputs = []
    inp_deque = deque(inp)

    while pc is not None:
        opcode = program[pc] % 100
        instr = IC_INSTRS[opcode]
        if instr.param_src == ParamSrc.INPUT:
            instr_inp = [inp_deque.popleft()]
        else:
            instr_inp = []
        er = instr.eval(program, pc, instr_inp)
        outputs += er.output
        for k, v in er.mem_change.items():
            program[k] = v
        pc = er.new_pc

    return outputs

def part1(output=False):
    base_program = parse()
    signals = []
    for amp_phase in permutations(range(5), 5):
        out = [0]
        for i in range(5):
            out = run_program(base_program, [amp_phase[i], out[0]])
        signals += [out[0]]
    return max(signals)

async def run_program_2(base_program, input_queue, output_queue):
    program = list(base_program)
    pc = 0

    last_out = None
    while pc is not None:
        opcode = program[pc] % 100
        instr = IC_INSTRS[opcode]
        if instr.param_src == ParamSrc.INPUT:
            instr_inp = [await input_queue.get()]
        else:
            instr_inp = []
        er = instr.eval(program, pc, instr_inp)
        if len(er.output) > 0:
            last_out = er.output[0]
            await output_queue.put(er.output[0])
        for k, v in er.mem_change.items():
            program[k] = v
        pc = er.new_pc

    return last_out

async def async_part2():
    base_program = parse()
    signals = []
    queues = [asyncio.Queue() for _ in range(5)]
    for amp_phase in permutations(range(5,10), 5):
        async with asyncio.TaskGroup() as tg:
            for i in range(5):
                inq  = queues[i - 1]
                outq = queues[i]
                await inq.put(amp_phase[i])
                if i == 0:
                    await inq.put(0)
                task = tg.create_task(run_program_2(base_program, inq, outq))
        signals += [await queues[-1].get()]

    return max(signals)

def part2(output=False):
    return asyncio.run(async_part2())

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())

