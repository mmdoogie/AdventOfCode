from functools import cache

with open('data/aoc_2021/21.txt') as f:
    startPos = [int(x.strip().split(' ')[4]) for x in f.readlines()]

class detdie:
    curr = 0
    cnt = 0
    
    def __init__(self):
        self.curr = 0
        self.cnt = 0
    
    def roll(self):
        rv = self.curr + 1
        self.curr = (self.curr + 1) % 100
        self.cnt += 1
        return rv

d = detdie()

def part1(output=False):
    scores = [0, 0]
    pos = [p-1 for p in startPos]
    while True:
        for i in range(2):
            rolls = [d.roll() for x in range(3)]
            move = sum(rolls)
            pos[i] = (pos[i] + move) % 10
            scores[i] += pos[i] + 1
            #print(f'Player {i} rolls {rolls} moves {move} pos {pos[i]} score {scores[i]}')
            if scores[i] >= 1000:
                break
        if any([sc >= 1000 for sc in scores]):
            break
    return min(scores) * d.cnt

dirac_rolls = []
for r1 in range(3):
    for r2 in range(3):
        for r3 in range(3):
            dirac_rolls += [r1 + r2 + r3 + 3]

@cache
def onemove(pos1, pos2, score1, score2):
    if score1 >= 21:
        return (1, 0)
    if score2 >= 21:
        return (0, 1)
    
    wins1 = 0
    wins2 = 0
    
    for roll in dirac_rolls:
        np = (pos1 + roll) % 10
        ns = score1 + np + 1
        (w2, w1) = onemove(pos2, np, score2, ns)
        wins1 += w1
        wins2 += w2
    
    return (wins1, wins2)

def part2(output=False):
    wins = onemove(startPos[0]-1, startPos[1]-1, 0, 0)
    return max(wins)
