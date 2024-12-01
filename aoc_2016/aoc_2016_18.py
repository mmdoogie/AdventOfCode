with open('data/aoc_2016/18.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    line1 = dat[0]
    linelen = len(line1)

def nextline(currline):
    nl = []
    for i in range(linelen):
        if i == 0:
            lrc = '.' + currline[i:i+2]
        elif i == linelen-1:
            lrc = currline[i-1:i+1] + '.'
        else:
            lrc = currline[i-1:i+2]
        if lrc in ['^^.', '.^^', '^..', '..^']:
            nl += ['^']
        else:
            nl += ['.']
    return ''.join(nl)

def process(linecount, output):
    line = line1
    s = sum(c == '.' for c in line)
    if output:
        print(f'{0:6} {line} {s} {s}')
    for i in range(linecount - 1):
        line = nextline(line)
        ds = sum(c == '.' for c in line)
        s += ds
        if output:
            print(f'{i + 1:6} {line} {ds} {s}')
    return s

def part1(output = True):
    return process(40, output)

def part2(output = True):
    return process(400000, output)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
