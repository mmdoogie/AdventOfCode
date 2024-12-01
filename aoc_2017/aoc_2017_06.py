with open('data/aoc_2017/06.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    init_banks = [int(x) for x in dat[0].split('\t')]
    bank_cnt = len(init_banks)

def distribute(start_banks):
    banks = list(start_banks)
    seen_cfgs = set()
    seen_cfgs.add(str(banks))
    cycles = 0

    while True:
        max_bank = max(banks)
        start_idx = banks.index(max_bank)
        blocks = banks[start_idx]
        banks[start_idx] = 0
        for b in range(blocks):
            banks[(start_idx + 1 + b) % bank_cnt] += 1
        cycles += 1
        cfg = str(banks)
        if cfg in seen_cfgs:
            break
        seen_cfgs.add(cfg)

    return cycles, banks

def part1(output = True):
    del output

    cycles, _banks = distribute(init_banks)
    return cycles

def part2(output = True):
    del output

    _cycles, banks = distribute(init_banks)
    cycles, _banks = distribute(banks)

    return cycles

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
