from collections import defaultdict
import operator

with open('data/aoc_2017/08.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def eval_cond(regfile, cond_reg, cond_type, cond_val):
    cond_fun = {'>':  operator.gt, '<':  operator.lt,
                '>=': operator.ge, '<=': operator.le,
                '==': operator.eq, '!=': operator.ne}

    if cond_type not in cond_fun:
        print('Undefined condition encountered!')
        return False

    return cond_fun[cond_type](regfile[cond_reg], int(cond_val))

def do_mod(regfile, mod_reg, mod_type, mod_val):
    mod_fun = {'inc': operator.add, 'dec': operator.sub}

    if mod_type not in mod_fun:
        print('Undefined modification encountered!')
        return None

    regfile[mod_reg] = mod_fun[mod_type](regfile[mod_reg], int(mod_val))
    return regfile[mod_reg]

def process():
    regfile = defaultdict(int)
    max_regval = 0

    for d in dat:
        parts = d.split(' ')

        if eval_cond(regfile, *parts[4:]):
            modded_val = do_mod(regfile, *parts[:3])
            max_regval = max(max_regval, modded_val)

    return max(regfile.values()), max_regval

def part1(output = True):
    del output

    final_max, _ = process()
    return final_max

def part2(output = True):
    del output

    _, all_max = process()
    return all_max

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
