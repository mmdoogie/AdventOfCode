from functools import cache
import random

with open('data/aoc_2021/23.txt') as f:
    dat = [x.strip() for x in f.readlines()]
row1a = [ord(x)-ord('A') for x in dat[2].split('#')[3:7]]
row2a = [ord(x)-ord('A') for x in dat[3].split('#')[1:5]]

class amphipod:
    last_pos = ('room', 0, 0)
    curr_pos = ('room', 0, 0)
    dest_room = 0
    weight = 1
    dist = 0
    max_depth = 1

    def __init__(self, pos, dest_room, max_depth = 1):
        self.last_pos = pos
        self.curr_pos = pos
        self.weight = 10**dest_room
        self.dest_room = dest_room
        self.max_depth = max_depth

    def __repr__(self):
        return (f'dst {self.dest_room} @ {self.curr_pos}')

    def energy(self):
        return self.weight * self.dist

    def move(self, pos):
        self.last_pos = self.curr_pos
        self.curr_pos = pos
        if self.curr_pos[0] == 'hall':
            self.dist += 1 + self.last_pos[2]
            if self.curr_pos[1] < 2*self.last_pos[1]:
                self.dist += 2*self.last_pos[1] - self.curr_pos[1]
            else:
                self.dist += self.curr_pos[1] - 2*self.last_pos[1]
        else:
            self.dist += 1 + self.curr_pos[2]
            if 2*self.curr_pos[1] < self.last_pos[1]:
                self.dist += self.last_pos[1] - 2*self.curr_pos[1]
            else:
                self.dist += 2*self.curr_pos[1] - self.last_pos[1]
    
    def valid_moves(self, pods):
        if self.curr_pos[0] == 'room' and self.last_pos[0] == 'hall':
            return []
        if self.curr_pos[0] == 'room':
            if self.curr_pos[2] >= 1 and any([p.curr_pos[0] == 'room' and p.curr_pos[1] == self.curr_pos[1] and p.curr_pos[2] < self.curr_pos[2] for p in pods]):
                return []
            left = [p.curr_pos[1] for p in pods if p.curr_pos[0] == 'hall' and p.curr_pos[1] <= 2*self.curr_pos[1] - 1]
            right = [p.curr_pos[1] for p in pods if p.curr_pos[0] == 'hall' and p.curr_pos[1] >= 2*self.curr_pos[1] + 1]
            if 2*self.curr_pos[1]-1 in left and 2*self.curr_pos[1]+1 in right:
                return []
            else:
                lpos = [('hall', x, 0) for x in range(-2 if len(left) == 0 else max(left)+1, 2*self.curr_pos[1]) if x not in [0,2,4,6]]
                rpos = [('hall', x, 0) for x in range(2*self.curr_pos[1]+1, 9 if len(right) == 0 else min(right)) if x not in [0,2,4,6]]
                return lpos + rpos
        else:
            occ = [p for p in pods if p.curr_pos[0] == 'room' and p.curr_pos[1] == self.dest_room]
            if any([p.dest_room != self.dest_room for p in occ]):
                return []
            if 2*self.dest_room < self.curr_pos[1]:
                if any([p.curr_pos[0] == 'hall' and p.curr_pos[1] in range(2*self.dest_room+1, self.curr_pos[1]) for p in pods]):
                    return []
            else:
                if any([p.curr_pos[0] == 'hall' and p.curr_pos[1] in range(self.curr_pos[1]+1, 2*self.dest_room) for p in pods]):
                    return []

            return [('room', self.dest_room, self.max_depth-len(occ))]

def random_game():
    pods = [amphipod(('room', i, 0), x) for i,x in enumerate(row1a)] + [amphipod(('room', i, 1), x) for i,x in enumerate(row2a)]

    moves = []
    
    while True:
        m = [(i, m) for i, p in enumerate(pods) for m in p.valid_moves(pods)]
        v = random.choice(m)
        pods[v[0]].move(v[1])
        moves += [v]
        if len(moves) > 50:
            return None
        if sum([len(p.valid_moves(pods)) for p in pods]) == 0:
            if all([p.curr_pos[0] == 'room' and p.curr_pos[1] == p.dest_room for p in pods]):
                return (sum([p.energy() for p in pods]), pods, moves)
            else:
                return None

def part1(output=False):
    random.seed(40)
    res = [random_game() for i in range(1000)]
    mv = min([r[0] for r in res if r is not None])
    return mv

MAX_DEPTH = 3

row1 = dat[2].split('#')[3:7]
row2 = dat[3].split('#')[1:5]

@cache
def valid_moves(state):
    moves = []
    for i, c in enumerate(state[0:11]):
        if c in 'ABCD':
            ridx = 11 + 4*(ord(c) - 65)
            samesies = [s == c.lower() for s in state[ridx:ridx+4] if s in 'abcdABCD']
            if not all(samesies):
                continue

            nrg = 0
            hidx = 2*(ord(c)-64)
            if hidx < i:
                if any([s in 'ABCD' for s in state[hidx:i]]):
                    continue
            else:
                if any([s in 'ABCD' for s in state[i+1:hidx+1]]):
                    continue

            dp = MAX_DEPTH - len(samesies)
            nrg += dp
            os = ridx + dp
            nm = state[0:i] + '-' + state[i+1:os] + c.lower() + state[os+1:]
            nrg *= 10**(ord(c)-65)
            moves += [(nrg, nm)]
    for r in range(4):
        ridx = 11 + 4*r
        for i, c in enumerate(state[ridx:ridx+4]):
            if c in 'ABCD':
                hidx = 2*(r+1)
                nrg = 1 + i

                left = [i for i, x in enumerate(state[0:hidx]) if x in 'ABCD']
                right = [i+hidx+1 for i, x in enumerate(state[hidx+1:11]) if x in 'ABCD']
                li = 0 if not left else max(left)+1
                ri = 11 if not right else min(right)

                ret_hidx = 2*(ord(c)-64)

                for l in range(li, hidx):
                    if l in [2,4,6,8]:
                        continue
                    nm = state[0:l] + c + state[l+1:ridx+i] + '_' + state[ridx+i+1:]
                    if l < ret_hidx:
                        ret_nrg = 1 + ret_hidx - l
                    else:
                        ret_nrg = 1 + l - ret_hidx
                    moves += [((10**(ord(c)-65))*(nrg + hidx-l + ret_nrg), nm)]

                for r in range(hidx+1, ri):
                    if r in [2,4,6,8]:
                        continue
                    nm = state[0:r] + c + state[r+1:ridx+i] + '_' + state[ridx+i+1:]
                    if r < ret_hidx:
                        ret_nrg = 1 + ret_hidx - r
                    else:
                        ret_nrg = 1 + r - ret_hidx
                    moves += [((10**(ord(c)-65))*(nrg + r-hidx + ret_nrg), nm)]

                break

    return moves

def solved(state):
    for r in range(4):
        ridx = 11 + 4*r
        if state[ridx] not in 'abcd':
            return False
    return True

def part2(output=False):
    curr_state = ''.join(['--x-x-x-x--',f'{row1[0]}DD{row2[0]}',f'{row1[1]}CB{row2[1]}',f'{row1[2]}BA{row2[2]}',f'{row1[3]}AC{row2[3]}'])

    to_do = valid_moves(curr_state)

    seen = 0
    min_r = 50000

    while len(to_do) > 0:

        seen += 1
        g = to_do.pop()

        nm = valid_moves(g[1])
        for n in nm:
            score = n[0] + g[0]
            if solved(n[1]):
                if score < min_r:
                    min_r = score
            elif score < min_r:
                to_do += [(score, n[1])]

    return min_r
