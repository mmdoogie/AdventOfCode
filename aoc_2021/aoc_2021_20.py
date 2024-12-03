with open('data/aoc_2021/20.txt') as f:
    dat = [x.strip() for x in f.readlines()]

algo = ['1' if c == '#' else '0' for c in dat[0]]
img = [['1' if c == '#' else '0' for c in l] for l in dat[2:]]

def getregion(img, x, y, dflt):
    h = len(img)
    w = len(img[0])
    rgn = ''
    
    for dy in [-1, 0, 1]:
        yy = y + dy
        for dx in [-1, 0, 1]:
            xx = x + dx
            if xx < 0 or yy < 0 or xx >= w or yy >= h:
                rgn += dflt
            else:
                rgn += img[yy][xx]
    
    return rgn

def ENHANCE(algo, img, dflt):
    h = len(img)
    w = len(img[0])
    
    ni = []
    
    for y in range(-1, h+1):
        l = []
        for x in range(-1, h+1):
            rs = getregion(img, x, y, dflt)
            rv = int(''.join(rs), 2)
            ov = algo[rv]
            l += [ov]
        ni += [l]

    return ni

def part1(output=False):
    s1 = ENHANCE(algo, img, '0')
    s2 = ENHANCE(algo, s1, '1')
    cnt = sum([sum([int(y) for y in x]) for x in s2])
    return cnt

def part2(output=False):
    s = [[y for y in x] for x in img]
    for n in range(50):
        dflt = '1' if n % 2 else '0'
        s = ENHANCE(algo, s, dflt)
    cnt2 = sum([sum([int(y) for y in x]) for x in s])
    return cnt2
