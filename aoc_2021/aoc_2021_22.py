import re

with open('data/aoc_2021/22.txt') as f:
    dat = [x.strip() for x in f.readlines()]
r = re.compile('([onf]{2,3}) x=([-0-9]*)\.\.([-0-9]*),y=([-0-9]*)\.\.([-0-9]*),z=([-0-9]*)\.\.([-0-9]*)')
cmds = [r.match(d).groups() for d in dat]

def part1(output=False):
    on_blocks = set()

    for c in cmds:
        xMin = int(c[1])
        xMax = int(c[2])
        yMin = int(c[3])
        yMax = int(c[4])
        zMin = int(c[5])
        zMax = int(c[6])
        
        for x in range(xMin, xMax+1):
            if x < -50 or x > 50:
                continue
            for y in range(yMin, yMax+1):
                if y < -50 or y > 50:
                    continue
                for z in range(zMin, zMax+1):
                    if z < -50 or z > 50:
                        continue
                    
                    if c[0] == 'on':
                        on_blocks.add((x,y,z))
                    else:
                        on_blocks.discard((x,y,z))

    return len(on_blocks)

class block_range:
    xMin = 0
    xMax = 0
    yMin = 0
    yMax = 0
    zMin = 0
    zMax = 0
    
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.xMin = min(x1,x2)
        self.xMax = max(x1,x2)
        self.yMin = min(y1,y2)
        self.yMax = max(y1,y2)
        self.zMin = min(z1,z2)
        self.zMax = max(z2,z2)
        
    def __repr__(self):
        return f'<x: {self.xMin}, {self.xMax}, y: {self.yMin}, {self.yMax}, z: {self.zMin}, {self.zMax}>'
    
    def size(self):
        return (self.xMax-self.xMin+1)*(self.yMax-self.yMin+1)*(self.zMax-self.zMin+1)

    def overlap(self, br2):
        rv = []

        if br2.xMin > self.xMax or br2.xMax < self.xMin or br2.yMin > self.yMax or br2.yMax < self.yMin or br2.zMin > self.zMax or br2.zMax < self.zMin:
            return None
        
        return block_range(max(self.xMin, br2.xMin), min(self.xMax, br2.xMax),
                           max(self.yMin, br2.yMin), min(self.yMax, br2.yMax),
                           max(self.zMin, br2.zMin), min(self.zMax, br2.zMax))

def part2(output=False):
    brs = []
    for c in cmds:
        x1, x2, y1, y2, z1, z2 = [int(v) for v in c[1:]]
        brs += [(c[0], block_range(x1, x2, y1, y2, z1, z2))]

    pos_blocks = []
    neg_blocks = []
    for c, b in brs:
        if c == 'on':
            nn = []
            np = [b]
            for p in pos_blocks:
                o = b.overlap(p)
                if o:
                    nn += [o]
            for n in neg_blocks:
                o = b.overlap(n)
                if o:
                    np += [o]
            pos_blocks += np
            neg_blocks += nn
        else:
            nn = []
            np = []
            for p in pos_blocks:
                o = b.overlap(p)
                if o:
                    nn += [o]
            for n in neg_blocks:
                o = b.overlap(n)
                if o:
                    np += [o]
            pos_blocks += np
            neg_blocks += nn

    total = sum([b.size() for b in pos_blocks]) - sum([b.size() for b in neg_blocks])
    return total
