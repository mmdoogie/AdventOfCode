import math
import itertools

from mrm.dijkstra import dijkstra

with open('data/aoc_2021/19.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def dist(pt1, pt2):
    return math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2+(pt1[2]-pt2[2])**2)

def tplus(pt1, pt2):
    return (pt1[0]+pt2[0], pt1[1]+pt2[1], pt1[2]+pt2[2])

def tminus(pt1, pt2):
    return (pt1[0]-pt2[0], pt1[1]-pt2[1], pt1[2]-pt2[2])

class report:
    i = None
    pts = []
    
    def __init__(self, i, lines):
        self.i = i
        self.pts = [[int(x) for x in l.split(',')] for l in lines]
        self.loc = (0, 0, 0)
    
    def modpts(self, conf, trans):
        np = [tplus(p, trans) for p in self.getpts(conf)]
        self.pts = np
        self.loc = tplus(report._trpt(self.loc, conf), trans)
    
    def _trpt(p, conf):
        # 0-3 : X+ Fwd
        if conf == 0:
            # X+ Fwd, Y+ Right, Z+ Down
            idx = [0, 1, 2]
            inv = [1, 1, 1]
            
        elif conf == 1:
            # X+ Fwd, Z+ Left, Y+ Down 
            idx = [0, 2, 1]
            inv = [1, -1, 1]
            
        elif conf == 2:
            # X+ Fwd, Y+ Left, Z+ Up
            idx = [0, 1, 2]
            inv = [1, -1, -1]
        
        elif conf == 3:
            # X+ Fwd, Z+ Right, Y+ Up
            idx = [0, 2, 1]
            inv = [1, 1, -1]
        
        # 4-7: X+ Rev
        elif conf == 4:
            # X+ Rev, Y+ Left, Z+ Down
            idx = [0, 1, 2]
            inv = [-1, -1, 1]
        
        elif conf == 5:
            # X+ Rev, Z+ Left, Y+ Up
            idx = [0, 2, 1]
            inv = [-1, -1, -1]
            
        elif conf == 6:
            # X+ Rev, Y+ Right, Z+ Up
            idx = [0, 1, 2]
            inv = [-1, 1, -1]
            
        elif conf == 7:
            # X+ Rev, Z+ Right, Y+ Down
            idx = [0, 2, 1]
            inv = [-1, 1, 1]
        
        # 8-11: X+ Right
        elif conf == 8:
            # Y+ Rev, X+ Right, Z+ Down
            idx = [1, 0, 2]
            inv = [-1, 1, 1]
            
        elif conf == 9:
            # Z+ Fwd, X+ Right, Y+ Down 
            idx = [2, 0, 1]
            inv = [1, 1, 1]
            
        elif conf == 10:
            # Y+ Fwd, X+ Right, Z+ Up
            idx = [1, 0, 2]
            inv = [1, 1, -1]
        
        elif conf == 11:
            # Z+ Rev, X+ Right, Y+ Up
            idx = [2, 0, 1]
            inv = [-1, 1, -1]
        
        # 12-15: X+ Left
        elif conf == 12:
            # Y+ Fwd, X+ Left, Z+ Down
            idx = [1, 0, 2]
            inv = [1, -1, 1]
        
        elif conf == 13:
            # Z+ Rev, X+ Left, Y+ Down
            idx = [2, 0, 1]
            inv = [-1, -1, 1]
            
        elif conf == 14:
            # Y+ Rev, X+ Left, Z+ Up
            idx = [1, 0, 2]
            inv = [-1, -1, -1]
            
        elif conf == 15:
            # Z+ Fwd, X+ Left, Y+ Up
            idx = [2, 0, 1]
            inv = [1, -1, -1]
        
        # 16-19: X+ Down
        elif conf == 16:
            # Z+ Rev, Y+ Right, X+ Down
            idx = [2, 1, 0]
            inv = [-1, 1, 1]
            
        elif conf == 17:
            # Y+ Rev, Z+ Left, X+ Down 
            idx = [1, 2, 0]
            inv = [-1, -1, 1]
            
        elif conf == 18:
            # Z+ Fwd, Y+ Left, X+ Down
            idx = [2, 1, 0]
            inv = [1, -1, 1]
        
        elif conf == 19:
            # Y+ Fwd, Z+ Right, X+ Down
            idx = [1, 2, 0]
            inv = [1, 1, 1]
        
        # 20-23: X+ Up
        elif conf == 20:
            # Z+ Fwd, Y+ Right, X+ Up
            idx = [2, 1, 0]
            inv = [1, 1, -1]
        
        elif conf == 21:
            # Y+ Rev, Z+ Right, X+ Up
            idx = [1, 2, 0]
            inv = [-1, 1, -1]
            
        elif conf == 22:
            # Z+ Rev, Y+ Left, X+ Up
            idx = [2, 1, 0]
            inv = [-1, -1, -1]
            
        elif conf == 23:
            # Y+ Fwd, Z+ Left, X+ Up
            idx = [1, 2, 0]
            inv = [1, -1, -1]
        
        return (p[idx[0]]*inv[0], p[idx[1]]*inv[1], p[idx[2]]*inv[2])

    def getpts(self, conf):
        return [report._trpt(p, conf) for p in self.pts]

def get_rpts():
    rpts = []
    lines = []
    i = -1
    for d in dat:
        if len(d) == 0:
            i += 1
            rpts += [report(i, lines)]
            lines = []
        elif not d.startswith('---'):
            lines += [d]
    if len(lines) != 0:
        i += 1
        rpts += [report(i, lines)]
    return rpts

def compute():
    rpts = get_rpts()
    params = []
    for r1, r2 in itertools.permutations(rpts, 2):
        p1 = r1.getpts(0)
        z1 = {int(1000 * round(dist(a, b), 3)): (a, b) for a, b in itertools.combinations(p1, 2)}
        p2 = r2.getpts(0)
        z2 = {int(1000 * round(dist(a, b), 3)): (a, b) for a, b in itertools.combinations(p2, 2)}
        m12 = set([a for k, v in z1.items() if k in z2 for a in v])
        if len(m12) >= 12:
            m120 = list(m12)[0]
            for c in range(24):
                p2 = r2.getpts(c)
                z2 = {int(1000 * round(dist(a, b), 3)): (a, b) for a, b in itertools.combinations(p2, 2)}
                m21 = set([a for k, v in z2.items() if k in z1 for a in v])
                for o1 in m21:
                    o = tminus(m120, o1)
                    d = sum([1 if int(dist(tminus(a, o), b))==0 else 0 for a in m12 for b in m21])
                    if d == 12:
                        params += [(r1.i, r2.i, c, o)]

    pmap = {(a,b): (c,d) for (a,b,c,d) in params}

    edges = [(p[0], p[1]) for p in params] + [(p[1], p[0]) for p in params]
    pts = set([x for p in params for x in p[0:2]])
    ngs = {p: [x[1] for x in edges if x[0] == p] for p in pts}

    weights, paths = dijkstra(ngs, start_point=0)

    psteps = {k: list(itertools.pairwise(reversed(v))) for k, v in paths.items()}
    allPoints = set(rpts[0].getpts(0))

    for i, r in enumerate(rpts):
        if i == 0:
            continue
        for s in psteps[i]:
            rs = (s[1], s[0])
            c, t = pmap[(rs)]
            r.modpts(c,t)
        allPoints.update(r.getpts(0))

    rlocs = [r.loc for r in rpts]
    maxDist = sorted([abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]) for a,b in itertools.combinations(rlocs, 2)], reverse=True)[0]

    return len(allPoints), maxDist

def part1(output=False):
    apl, _ = compute()
    return apl

def part2(output=False):
    _, maxDist = compute()
    return maxDist
