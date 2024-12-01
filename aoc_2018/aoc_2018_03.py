import re

with open('data/aoc_2018/03.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output = True):
    regex = re.compile('#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)')
    claim_counts = {}
    for d in dat:
        m = regex.match(d)
        if output:
            print(d, m.groups())
        ci, cx, cy, cw, ch = [int(x) for x in m.groups()]
        for y in range(cy, cy + ch):
            for x in range(cx, cx + cw):
                if (x, y) in claim_counts:
                    claim_counts[(x, y)] += 1
                else:
                    claim_counts[(x, y)] = 1
    overlaps = [c for c in claim_counts.values() if c != 1]
    return len(overlaps)

def part2(output = True):
    regex = re.compile('#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)')
    claims = {}
    for d in dat:
        m = regex.match(d)
        ci, cx, cy, cw, ch = [int(x) for x in m.groups()]
        claims[ci] = (cx, cy, cw, ch)

    for c1k, c1v in claims.items():
        overlapped = False
        for c2k, c2v in claims.items():
            if c1k == c2k:
                continue
            c1x1 = c1v[0]
            c1x2 = c1v[0] + c1v[2] - 1
            c1y1 = c1v[1]
            c1y2 = c1v[1] + c1v[3] - 1
            
            c2x1 = c2v[0]
            c2x2 = c2v[0] + c2v[2] - 1
            c2y1 = c2v[1]
            c2y2 = c2v[1] + c2v[3] - 1

            if (c2x1 >= c1x1 and c2x1 <= c1x2) or (c2x2 >= c1x1 and c2x2 <= c1x2) or (c2x1 <= c1x1 and c2x2 >= c1x2):
                if (c2y1 >= c1y1 and c2y1 <= c1y2) or (c2y2 >= c1y1 and c2y2 <= c1y2) or (c2y1 <= c1y1 and c2y2 >= c1y2):
                    if output:
                        print(f'{c1k} overlapped by {c2k}')
                    overlapped = True
                    break
        if not overlapped:
            return c1k
