from hashlib import md5

with open('data/aoc_2016/05.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    idx = 0
    codes = ''
    while True:
        h = md5((dat[0] + str(idx)).encode('utf-8')).hexdigest()
        if h.startswith('00000'):
            codes += h[5]
            if output:
                print(f"{idx:10} {codes}")
        if len(codes) == 8:
            break
        idx += 1

    return codes

def part2(output = True):
    idx = 0
    codes = ['_'] * 8
    while True:
        h = md5((dat[0] + str(idx)).encode('utf-8')).hexdigest()
        if h.startswith('00000') and h[5] in '01234567' and codes[int(h[5])] == '_':
            codes[int(h[5])] = h[6]
            if output:
                print(f"{idx:10} {''.join(codes)}")
        if '_' not in codes:
            break
        idx += 1

    return ''.join(codes)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
