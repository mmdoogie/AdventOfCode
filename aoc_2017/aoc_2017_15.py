with open('data/aoc_2017/15.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    gen_a_iv = int(dat[0].split('with ')[1])
    gen_b_iv = int(dat[1].split('with ')[1])

def generator(factor, iv, size, filt_factor = 1):
    val = iv
    for _ in range(size):
        val = (val * factor) % 2147483647
        if filt_factor != 1:
            while val % filt_factor != 0:
                val = (val * factor) % 2147483647
        yield val & 0xFFFF

def part1(output = True):
    del output

    gen_a = generator(16807, gen_a_iv, 40000000)
    gen_b = generator(48271, gen_b_iv, 40000000)

    matches = sum(av == bv for av, bv in zip(gen_a, gen_b))
    return matches

def part2(output = True):
    del output

    gen_a = generator(16807, gen_a_iv, 5000000, 4)
    gen_b = generator(48271, gen_b_iv, 5000000, 8)

    matches = sum(av == bv for av, bv in zip(gen_a, gen_b))
    return matches

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
