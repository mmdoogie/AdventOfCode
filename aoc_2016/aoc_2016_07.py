import re

with open('data/aoc_2016/07.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

supernet_pat = re.compile(r'(?:\]|^)([a-z]+)\[?')
hypernet_pat = re.compile(r'\[([a-z]+)\]')

def part1(output = True):
    tcnt = 0
    for d in dat:
        snet = supernet_pat.findall(d)
        hnet = hypernet_pat.findall(d)
        if output:
            print('Address:', d)
            print('Supernets:', snet)
            print('Hypernets:', hnet)

        snet_abbas = False
        for s in snet:
            for i in range(0, len(s) - 3):
                if s[i] == s[i + 3] and s[i] != s[i + 1] and s[i + 1] == s[i + 2]:
                    snet_abbas = True
                    if output:
                        print('Found supernet ABBA', s[i:i+4])
                    break
            if snet_abbas:
                break
        if not snet_abbas:
            if output:
                print()
            continue

        hnet_abbas = False
        for h in hnet:
            for i in range(0, len(h) - 3):
                if h[i] == h[i + 3] and h[i] != h[i + 1] and h[i + 1] == h[i + 2]:
                    hnet_abbas = True
                    if output:
                        print('Found hypernet ABBA', h[i:i+4], 'disqualified!')
                        print()
                    break
            if hnet_abbas:
                break
        if hnet_abbas:
            continue

        if output:
            print('Supports TLS!')
            print()
        tcnt += 1

    return tcnt

def part2(output = True):
    scnt = 0
    for d in dat:
        snet = supernet_pat.findall(d)
        hnet = hypernet_pat.findall(d)
        if output:
            print('Address:', d)
            print('Supernets:', snet)
            print('Hypernets:', hnet)

        snet_abas = []
        for s in snet:
            for i in range(0, len(s) - 2):
                if s[i] == s[i + 2] and s[i] != s[i + 1]:
                    snet_abas += [s[i : i + 3]]
        if output:
            if snet_abas:
                print('Supernet ABAs:', snet_abas)
            else:
                print()
        if not snet_abas:
            continue

        hnet_abas = []
        for h in hnet:
            for i in range(0, len(h) - 2):
                if h[i] == h[i + 2] and h[i] != h[i + 1]:
                    hnet_abas += [h[i + 1] + h[i] + h[i + 1]]
        if output:
            if hnet_abas:
                print('Hypernet BABs (inverted):', hnet_abas)
            else:
                print()
        if not hnet_abas:
            continue

        if any(s in hnet_abas for s in snet_abas):
            if output:
                print('Supports SSL!')
                print()
            scnt += 1
        elif output:
            print('No match.')
            print()

    return scnt

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
