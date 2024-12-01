
with open('data/aoc_2016/09.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def decomplen(d, v2):
    idx = 0
    dclen = 0
    sz = len(d)

    while True:
        while idx < sz and d[idx] != '(':
            dclen += 1
            idx += 1
        if idx == sz:
            break

        idx += 1
        char_cnt = ''
        while d[idx] != 'x':
            char_cnt += d[idx]
            idx += 1
        char_cnt = int(char_cnt)

        idx += 1
        dat_size = ''
        while d[idx] != ')':
            dat_size += d[idx]
            idx += 1
        dat_size = int(dat_size)

        idx += 1
        if v2:
            substr = d[idx:idx + char_cnt]
            substr_dclen = decomplen(substr, True)
            dclen += substr_dclen * dat_size
        else:
            dclen += char_cnt * dat_size

        idx += char_cnt

    return dclen

def part1(output = True):
    del output
    return decomplen(dat[0], False)

def part2(output = True):
    del output
    return decomplen(dat[0], True)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
