with open('data/aoc_2015/14.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    deer = {}
    for d in dat:
        p = d.split(' ')
        n = p[0]
        v = int(p[3])
        tv = int(p[6])
        tr = int(p[13])
        deer[n] = (v, tv, tr)
    return deer

def calc_dist(deer, time):
    period = deer[1] + deer[2]
    dist = deer[0] * deer[1]
    full = time // period * dist
    rem = min(time % period, deer[1]) * deer[0]
    return full + rem

def part1(output = True):
    deer = parse()
    dists = [calc_dist(d, 2503) for d in deer.values()]
    return max(dists)

def part2(output = True):
    deer = parse()
    scores = {d: 0 for d in deer}
    for i in range(1, 2503 + 1):
        dists = {k: calc_dist(v, i) for k, v in deer.items()}
        winner = max(dists.items(), key=lambda x: x[1])[0]
        scores[winner] += 1
    return max(scores.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
