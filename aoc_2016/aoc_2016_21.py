with open('data/aoc_2016/21.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def rbop_tbl():
    bb = 'abcdefgh'
    rev_tbl = {}
    for i, b in enumerate(bb):
        scram = list(bb)
        steps = scram.index(b)
        if steps >= 4:
            steps = (steps + 2) % len(bb)
        else:
            steps = (steps + 1) % len(bb)
        scram = scram[-steps:] + scram[:-steps]
        endpos = scram.index(b)
        rev_tbl[endpos] = i - endpos
    return rev_tbl

def process(base_str, instrs, output):
    scram = list(base_str)
    if output:
        print(f'{"":50}', ''.join(scram))

    rev_tbl = rbop_tbl()

    for d in instrs:
        match d.split(' '):
            case ['swap', 'letter', l1, 'with', 'letter', l2]:
                idx = [scram.index(l1), scram.index(l2)]
                idx.sort()
                scram = scram[:idx[0]] + [scram[idx[1]]] + scram[idx[0]+1:idx[1]] + [scram[idx[0]]] + scram[idx[1]+1:]
            case ['swap', 'position', p1, 'with', 'position', p2]:
                idx = [int(p1), int(p2)]
                idx.sort()
                scram = scram[:idx[0]] + [scram[idx[1]]] + scram[idx[0]+1:idx[1]] + [scram[idx[0]]] + scram[idx[1]+1:]
            case ['rotate', side, n1, _]:
                steps = int(n1)
                if side == 'right':
                    steps *= -1
                scram = scram[steps:] + scram[:steps]
            case ['move', 'position', p1, 'to', 'position', p2]:
                fp = int(p1)
                tp = int(p2)
                if fp < tp:
                    scram = scram[:fp] + scram[fp+1:tp+1] + [scram[fp]] + scram[tp+1:]
                else:
                    scram = scram[:tp] + [scram[fp]] + scram[tp:fp] + scram[fp+1:]
            case ['rotate', 'based', 'on', 'position', 'of', 'letter', l1]:
                steps = scram.index(l1)
                if steps >= 4:
                    steps = (steps + 2) % len(base_str)
                else:
                    steps = (steps + 1) % len(base_str)
                scram = scram[-steps:] + scram[:-steps]
            case ['reverse', 'positions', p1, 'through', p2]:
                idx = [int(p1), int(p2)]
                idx.sort()
                scram = scram[:idx[0]] + list(reversed(scram[idx[0]:idx[1]+1])) + scram[idx[1]+1:]
            case ['rbop', l1]:
                idx = scram.index(l1)
                steps = -rev_tbl[idx]
                scram = scram[steps:] + scram[:steps]
        if output:
            print(f'{d:50}', ''.join(scram))

    return ''.join(scram)

def part1(output = True):
    base_str = 'abcdefgh'
    return process(base_str, dat, output)

def part2(output = True):
    base_str = 'fbgdceah'
    revdat = []
    for d in reversed(dat):
        if 'swap' in d or 'reverse' in d:
            revdat += [d]
        elif 'left' in d:
            spl = d.split('left')
            revdat += [''.join([spl[0], 'right', spl[1]])]
            continue
        elif 'right' in d:
            spl = d.split('right')
            revdat += [''.join([spl[0], 'left', spl[1]])]
            continue
        elif 'move' in d:
            spl = d.split(' ')
            revdat += [' '.join(spl[0:2] + [spl[5]] + spl[3:5] + [spl[2]])]
            continue
        elif 'based' in d:
            spl = d.split('letter ')
            revdat += [f'rbop {spl[1]}']
        else:
            pass
    return process(base_str, revdat, output)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
